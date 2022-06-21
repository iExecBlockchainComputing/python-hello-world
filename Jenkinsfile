@Library('global-jenkins-library@2.0.0') _

buildInfo = getBuildInfo()

def nativeImage = buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: 'cloud-computing',
  buildContext: 'cloud-computing',
  dockerImageRepositoryName: 'python-hello-world',
  visibility: 'docker.io'
)

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
)
