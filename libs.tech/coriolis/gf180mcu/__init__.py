
from pathlib import Path
from coriolis.designflow.technos import Where
from coriolis.designflow.task    import ShellEnv


__all__ = [ 'setup', 'pdkGFTop' ]


pdkMasterTop = None
pdkGFTop     = None


def setup ( checkToolkit=None, useHV=False ):
    global pdkMasterTop
    global pdkGFTop

    from coriolis                     import Cfg 
    from coriolis                     import Viewer
    from coriolis                     import CRL 
    from coriolis.helpers             import overlay, l, u, n
    from coriolis.designflow.yosys    import Yosys
    from coriolis.designflow.klayout  import Klayout
    from coriolis.designflow.tasyagle import TasYagle
    from .techno                      import setup as techno_setup 
    from .mcu9t5v0                    import setup as StdCellLib_setup
    from .iolib                       import setup as iolib_setup

    pdkGFTop = Path( __file__ ).parent

    Where( checkToolkit )

    techno_setup( useHV )
    StdCellLib_setup( pdkGFTop, useHV )
    iolib_setup( pdkGFTop )
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.misc.catchCore           = False
        cfg.misc.minTraceLevel       = 12300
        cfg.misc.maxTraceLevel       = 12400
        cfg.misc.info                = False
        cfg.misc.paranoid            = False
        cfg.misc.bug                 = False
        cfg.misc.logMode             = True
        cfg.misc.verboseLevel1       = False
        cfg.misc.verboseLevel2       = False
        cfg.etesian.graphics         = 2
        cfg.anabatic.topRoutingLayer = 'Metal5'
        cfg.katana.eventsLimit       = 4000000
        af  = CRL.AllianceFramework.get()
       #lg5 = af.getRoutingGauge( 'mcu9t' ).getLayerGauge( 5 ) 
       #lg5.setType( CRL.RoutingLayerGauge.PowerSupply )
        env = af.getEnvironment()
        env.setCLOCK( '^sys_clk$|^ck|^jtag_tck$' )

    cellsTop = pdkGFTop / 'libraries' / 'gf180mcu_fd_sc_mcu9t5v0' / 'latest' / 'cells'
   #liberty  = pdkGFTop / 'libraries' / 'gf180mcu_fd_sc_mcu9t5v0' / 'latest' / 'liberty' / 'gf180mcu_fd_sc_mcu9t5v0__tt_025C_5v00.lib'
    liberty  = pdkGFTop / 'mcu9t5v0.lib'

    Yosys.setLiberty( liberty )
    ShellEnv.CHECK_TOOLKIT = Where.checkToolkit.as_posix()
