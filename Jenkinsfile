@Library('global-jenkins-library@2.0.0') _

buildInfo = getBuildInfo()

baseDir = 'cloud-computing'
nativeImage = buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: baseDir,
  buildContext: baseDir,
  dockerImageRepositoryName: 'python-hello-world',
  visibility: 'docker.io'
)

buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: baseDir + '/gramine',
  buildContext: baseDir,
  dockerImageRepositoryName: 'tee-gramine-python-hello-world',
  visibility: 'iex.ec'
)


sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
)
