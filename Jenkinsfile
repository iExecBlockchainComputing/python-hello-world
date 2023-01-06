@Library('global-jenkins-library@feature/docker-build-options') _

buildInfo = getBuildInfo()

baseDir = 'cloud-computing'
nativeImage = buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: baseDir,
  buildContext: baseDir,
  dockerImageRepositoryName: 'python-hello-world',
  visibility: 'docker.io'
)

stage('Build Gramine images') {
    dockerfileDir = baseDir + '/gramine'
    dockerImageRepositoryName = 'tee-gramine-python-hello-world'
    visibility = 'iex.ec'
    // Production image
    productionImageName = buildSimpleDocker_v3(
        buildInfo: buildInfo,
        dockerfileDir: dockerfileDir,
        buildContext: baseDir,
        dockerImageRepositoryName: dockerImageRepositoryName,
        visibility: visibility
    )
    // Test CA image
    buildInfo.imageTag = buildInfo.imageTag + '-test-ca'
    buildSimpleDocker_v3(
        buildInfo: buildInfo,
        dockerfileDir: dockerfileDir,
        dockerfileFilename: 'Dockerfile.test-ca',
        dockerBuildOptions: '--build-arg BASE_IMAGE=' + productionImageName,
        dockerImageRepositoryName: dockerImageRepositoryName,
        visibility: visibility
    )
}

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
  sconifyVersion:  '5.7.1'
)
