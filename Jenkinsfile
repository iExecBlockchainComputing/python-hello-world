@Library('global-jenkins-library@1.6.1') _

def tasks = [:]
tasks["cloud"] = {
    stage ("Build Python Hello World"){
        def nativeImage = buildSimpleDocker_v2(dockerfileDir: 'cloud-computing',
                dockerImageRepositoryName: 'python-hello-world', imageprivacy: 'public')
        sconeBuildAllTee(nativeImage: nativeImage, targetImageRepositoryName: 'python-hello-world',
                sconifyArgsPath: 'cloud-computing/sconify.args')
    }
}
parallel tasks
