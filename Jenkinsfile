@Library('global-jenkins-library@2.3.1') _

buildInfo = getBuildInfo()
dockerIoVisibility = Registries.EXTERNAL_DOCKERIO_HOST

properties(
    [
        buildDiscarder(logRotator(numToKeepStr: '10')),
        parameters([
                string(defaultValue: '5.7.6', name: 'SCONIFY_VERSION', trim: true)
        ])
    ]
)

if (params.SCONIFY_VERSION == null || params.SCONIFY_VERSION = '') {
    error "SCONIFY_VERSION can't be null or empty"
}

baseDir = 'cloud-computing'
nativeImage = buildSimpleDocker_v3(
  buildInfo: buildInfo,
  dockerfileDir: baseDir,
  buildContext: baseDir,
  dockerImageRepositoryName: 'python-hello-world',
  visibility: dockerIoVisibility
)

stage('Build Gramine') {
    gramineBuildInfo = buildInfo.clone()
    dockerfileDir = baseDir + '/gramine'
    dockerImageRepositoryName = 'tee-python-hello-world'
    gramineBuildInfo.imageTag += '-gramine'
    productionImageName = ''
    stage('Build Gramine production image') {
        productionImageName = buildSimpleDocker_v3(
            buildInfo: gramineBuildInfo,
            dockerfileDir: dockerfileDir,
            buildContext: baseDir,
            dockerImageRepositoryName: dockerImageRepositoryName,
            visibility: dockerIoVisibility
        )
    }
    stage('Build Gramine test CA image') {
        testCaSuffix = 'test-ca'
        gramineBuildInfo.imageTag += '-' + testCaSuffix
        buildSimpleDocker_v3(
            buildInfo: gramineBuildInfo,
            dockerfileDir: dockerfileDir,
            dockerfileFilename: 'Dockerfile.' + testCaSuffix,
            dockerBuildOptions: '--build-arg BASE_IMAGE=' + productionImageName,
            dockerImageRepositoryName: dockerImageRepositoryName,
            visibility: Registries.EXTERNAL_IEXEC_HOST
        )
    }
}

sconeBuildUnlocked(
  nativeImage:     nativeImage,
  imageName:       'python-hello-world',
  imageTag:        buildInfo.imageTag,
  sconifyArgsPath: 'cloud-computing/sconify.args',
  sconifyVersion:  params.SCONIFY_VERSION
)
