
   packageName="coriolis-pdk-gf180mcu"
    venvVersion="2.5.5"
   venvSnapshot="venv-al9-${venvVersion}.tar.gz"
        version="2025.07.21"
      obsCI_CNT="9"
       obsB_CNT="1"

 rpmSources=""
 rpmSources="${rpmSources} packaging/coriolis-pdk-gf180mcu.spec"
 rpmSources="${rpmSources} packaging/coriolis-pdk-gf180mcu-rpmlintrc"
 rpmSources="${rpmSources} packaging/patchvenv.sh"
 rpmSources="${rpmSources} ${venvSnapshot}"
 rpmSources="${rpmSources} coriolis-pdk-gf180mcu-${version}.tar.gz"

 debSources=""
 debSources="${debSources} packaging/coriolis-pdk-gf180mcu.dsc"
 debSources="${debSources} packaging/debian.changelog"
 debSources="${debSources} packaging/debian.control"
 debSources="${debSources} packaging/debian.copyright"
 debSources="${debSources} packaging/debian.rules"


 echo "Running uploadOBSs.sh"

 source ./packaging/uploadUtils.sh

     doVEnv="false"
   doCommit="false"

 parseArguments $*
 simpleBuildArchive
 runDoVEnv
 copyFiles
 buildObs
 buildLocalRpm
