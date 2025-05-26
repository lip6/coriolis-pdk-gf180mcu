
import sys
import os.path
from   coriolis                 import Cfg
from   coriolis.Hurricane       import Technology, DataBase, DbU, Library, Layer,            \
                                       BasicLayer, Cell, Net, Horizontal, Vertical, Contact, \
                                       Rectilinear, Box, Point, Instance, Transformation,    \
                                       NetExternalComponents, Pad, Path, Query
import coriolis.Viewer
from   coriolis.CRL             import AllianceFramework, Gds, LefImport, CellGauge,  \
                                       RoutingGauge, RoutingLayerGauge
from   coriolis.Anabatic        import StyleFlags
from   coriolis.helpers         import trace, l, u, n, overlay, io, ndaTopDir
from   coriolis.helpers.overlay import CfgCache, UpdateSession


__all__ = [ 'setup' ]


def _routing ():
    """
    Define the routing gauge for I/O cells along with the various P&R tool parameters.
    """
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        cfg.chip.supplyRailWidth = 4*u(5.04)
        cfg.chip.supplyRailPitch = 8*u(5.04)
        cfg.chip.padCoreSide     = 'North'
        cfg.chip.ioPadGauge      = 'LEF.GF_IO_Site'
    af = AllianceFramework.get()
    cg = CellGauge.create( 'LEF.GF_IO_Site'
                         , 'Metal2'  # pin layer name.
                         , u(  1.0)  # pitch.
                         , u(350.0)  # cell slice height.
                         , u( 75.0)  # cell slice step.
                         )
    af.addCellGauge( cg )


def _loadIoLib ( pdkDir ):
    """
    Load the I/O cells from the LEF+GDS files.
    """
    af       = AllianceFramework.get()
    db       = DataBase.getDB()
    tech     = db.getTechnology()
    rootlib  = db.getRootLibrary()
    ioLib    = Library.create( rootlib, 'iolib' )
    ioLibGds = Library.create( ioLib  , 'GDS'     )
    LefImport.setMergeLibrary( ioLib )
    LefImport.setGdsForeignLibrary( ioLibGds )
    #LefImport.load( (pdkDir / 'libraries'
    #                        / 'gf180mcu_fd_sc_mcu9t5v0'
    #                        / 'latest'
    #                        / 'tech'
    #                        / 'gf180mcu_6LM_1TM_9K_9t_tech.lef').as_posix() )
    io.vprint( 1, '  o  Setup GF180MCU I/O library in {}.'.format( ioLib.getName() ))
    cellsDir = pdkDir / 'libraries' / 'gf180mcu_fd_io' / 'latest' / 'cells'
    for lefFile in cellsDir.glob( '*/*_5lm.lef' ):
        io.vprint( 2, '        - I/O pad <{}>.'.format( lefFile ))
        gdsFile = lefFile.with_suffix( '.gds' )
        if gdsFile.is_file():
            io.vprint( 2, '        - I/O pad <{}>.'.format( gdsFile ))
            Gds.setTopCellName( gdsFile.stem[:-4] )
            Gds.load( ioLibGds, gdsFile.as_posix(), Gds.Layer_0_IsBoundary|Gds.NoBlockages|Gds.LefForeign )
        LefImport.load( lefFile.as_posix() )
    # Demote the VDD/VSS nets until we understand how that works.
    for cell in ioLib.getCells():
        for net in cell.getNets():
            if net.getName() in ('VDD', 'VSS'):
                net.setExternal( False )
                net.setGlobal( False )
    af.wrapLibrary( ioLib, 1 ) 


def setup ( pdkDir ):
   #with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
   #    cfg.misc.minTraceLevel = 100
   #    cfg.misc.maxTraceLevel = 102
    _routing()
    _loadIoLib( pdkDir )
