multibranchPipelineJob('perform-health-check') {
    displayName('perform_health_check_pipeline')
    branchSources {
        git {
            id('123456789-perform-health-check') // IMPORTANT: use a constant and unique identifier
            remote('https://github.com/csye7125-fall2023-group08/perform-health-check.git')
            credentialsId('token-github')
            configure { node ->
                def webhookTrigger = node / triggers / 'com.igalg.jenkins.plugins.mswt.trigger.ComputedFolderWebHookTrigger' {
                    spec('')
                    token("perform-health-check")
                }
            }
        }
    }
    configure {
        def traitBlock = it / 'sources' / 'data' / 'jenkins.branch.BranchSource' / 'source' / 'traits'
        traitBlock << 'jenkins.plugins.git.traits.CloneOptionTrait' {
            extension(class: 'hudson.plugins.git.extensions.impl.CloneOption') {
                shallow(false)
                noTag(false)
                reference()
                depth(0)
                honorRefspec(false)
            }
        }

        traitBlock << 'jenkins.plugins.git.traits.BranchDiscoveryTrait' { }
    }
}