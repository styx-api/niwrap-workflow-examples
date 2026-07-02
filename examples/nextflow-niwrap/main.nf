/*
 * NiWrap + Nextflow example workflow.
 *
 * This pipeline runs the same minimal neuroimaging pipeline as the other
 * examples: FSL BET skull-stripping, ANTs N4 bias-field correction, and ANTs
 * registration to the MNI152NLin2009cAsym template.
 *
 * The Python helper scripts in src/nextflow_niwrap/ call NiWrap and are
 * executed through the command configured in params.python_cmd (see
 * nextflow.config).
 */

nextflow.enable.dsl = 2


process ANATOMICAL_PREPROCESS {
    /* Skull-strip and bias-field correct a subject's T1w image. */

    publishDir "${params.output_dir}/preprocess", mode: 'copy'

    input:
        tuple val(meta), path(t1w)

    output:
        tuple val(meta), path("sub-${meta.subject}_desc-preproc_T1w.nii.gz"), emit: preproc_t1w

    script:
    def bet_arg = params.bet_fractional_intensity != null ? "--bet-fractional-intensity ${params.bet_fractional_intensity}" : ""
    """
    ${params.python_cmd} ${projectDir}/src/nextflow_niwrap/preprocess.py \\
        --t1w "${t1w}" \\
        --output "sub-${meta.subject}_desc-preproc_T1w.nii.gz" \\
        ${bet_arg}
    """
}


process REGISTRATION_TO_TEMPLATE {
    /* Register the preprocessed T1w image to the template space. */

    publishDir "${params.output_dir}/registration", mode: 'copy'

    input:
        tuple val(meta), path(preproc_t1w), path(template_t1w)

    output:
        tuple val(meta), path("sub-${meta.subject}_space-${params.template}_desc-preproc_T1w.nii.gz"), emit: xfm_t1w

    script:
    """
    ${params.python_cmd} ${projectDir}/src/nextflow_niwrap/register.py \\
        --moving "${preproc_t1w}" \\
        --fixed "${template_t1w}" \\
        --output "sub-${meta.subject}_space-${params.template}_desc-preproc_T1w.nii.gz"
    """
}


workflow {
    def subjects = params.subject instanceof List ? params.subject : [params.subject]

    t1w_ch = Channel.fromList(subjects)
        .map { subject ->
            tuple(
                [subject: subject],
                file("${params.data_dir}/ds000001/sub-${subject}/anat/sub-${subject}_T1w.nii.gz")
            )
        }

    template_ch = Channel.fromPath(
        "${params.data_dir}/templateflow/tpl-${params.template}/tpl-${params.template}_res-01_T1w.nii.gz"
    )

    ANATOMICAL_PREPROCESS(t1w_ch)
    REGISTRATION_TO_TEMPLATE(
        ANATOMICAL_PREPROCESS.out.preproc_t1w.combine(template_ch)
    )
}
