#!/bin/sh

    rootDir="${HOME}/coriolis-2.x"
   buildDir="${rootDir}/release/build-gf180mcu"
 installDir="${rootDir}/release/install"
 rm -rf ${buildDir}
 rm -rf ${installDir}/lib64/python3.9/site-packages/pdks/gf180mcu
 meson setup --prefix ${installDir} ${buildDir}
 meson install -C ${buildDir}
