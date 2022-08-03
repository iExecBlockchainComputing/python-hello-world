@Library('global-jenkins-library@2.1.1') _

buildInfo = getBuildInfo()

def nativeImage = buildSimpleDocker_v2(
  buildInfo: buildInfo,
  dockerfileDir: 'cloud-computing',
  dockerImageRepositoryName: 'python-hello-world',
  imageprivacy: 'public'
)

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
  sconifyVersion:  '5.7.1'
)
