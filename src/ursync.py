#!/usr/bin/python
'''Script to perform rsync using offline storage'''


import sys
import gflags

gflags.DEFINE_bool(
    name = 'verbose',
    short_name = 'v',
    help = "Show verbose output",
    default = False)

gflags.DEFINE_bool(
    name = 'list_files',
    short_name = 'F',
    help = "List each file being processed",
    default = False)

gflags.DEFINE_bool(
    name = 'target',
    default = False,
    help = "Specifies that this is being run on the target host")

gflags.DEFINE_bool(
    name = 'source',
    default = False,
    help = "Specifies that this is being run on the source host")

gflags.DEFINE_integer(
    name = 'block_size',
    short_name = 'B',
    default = 4096,
    help = "Specify the block size to use when searching files for existing data",
    )

from rsync_usb.cmds.TargetCommand import TargetCommand
from rsync_usb.cmds.SourceCommand import SourceCommand

from rsync_usb.ui.ConsoleUI import ConsoleUI

from rsync_usb.ParameterError import ParameterError

if __name__ == '__main__':

    ui = ConsoleUI()

    # Parse arguments
    try:
        argv = gflags.FLAGS(sys.argv)

        # Arguments
        if len(argv) != 3:
            raise gflags.FlagsError("Must specify paths")
        local_path, trx_path = argv[1:]

        # Either --target or --source
        if not gflags.FLAGS.target and not gflags.FLAGS.source:
            raise gflags.FlagsError("Must specify either --target or --source")

    except gflags.FlagsError, e:
        ui.usage_error(str(e))
        sys.exit(1)

    ui.inform_version()

    try:
        cmd = None
        if gflags.FLAGS.target:
            cmd = TargetCommand(trx_path)
        elif gflags.FLAGS.source:
            cmd = SourceCommand(trx_path)
        else:
            ui.abort("Nothing to do?")
            sys.exit(1)

        if gflags.FLAGS.verbose:
            cmd.opt_verbose = True

        if gflags.FLAGS.list_files:
            cmd.opt_list_files = True

        if gflags.FLAGS.block_size is not None:
            cmd.opt_default_block_size = int(gflags.FLAGS.block_size)

        cmd.run(local_path)


    except ParameterError, e:
        ui.abort(str(e))
        sys.exit(1)

    ui.inform("Finished")


