@Library('global-jenkins-library@feature/standalone-scone-build') _

buildInfo = getBuildInfo()

def nativeImage = buildSimpleDocker_v2(
  buildInfo: buildInfo,
  dockerfileDir: 'cloud-computing',
  dockerImageRepositoryName: 'python-hello-world',
  imageprivacy: 'private'
)

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
)
