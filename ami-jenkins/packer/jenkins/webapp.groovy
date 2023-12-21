multibranchPipelineJob('webapp') {
    displayName('webapp_pipeline')
    branchSources {
        git {
            id('123456789-webapp') // IMPORTANT: use a constant and unique identifier
            remote('https://github.com/csye7125-fall2023-group08/webapp.git')
            credentialsId('token-github')
            configure { node ->
                def webhookTrigger = node / triggers / 'com.igalg.jenkins.plugins.mswt.trigger.ComputedFolderWebHookTrigger' {
                    spec('')
                    token("webapp")
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


