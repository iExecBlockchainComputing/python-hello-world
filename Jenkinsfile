@Library('global-jenkins-library@2.3.1') _

buildInfo = getBuildInfo()

properties(
    [
        buildDiscarder(logRotator(numToKeepStr: '10')),
        parameters([
                string(defaultValue: '5.9.1', name: 'SCONIFY_VERSION', trim: true)
        ])
    ]
)

if (params.SCONIFY_VERSION.isBlank()) {
    error "SCONIFY_VERSION can't be null or empty"
}

baseDir = 'cloud-computing'
nativeImage = buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: baseDir,
  buildContext: baseDir,
  dockerImageRepositoryName: 'python-hello-world',
  visibility: 'iex.ec'
)

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
  sconifyVersion:  params.SCONIFY_VERSION
)
