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


process anatomical_preprocess {
    /* Skull-strip and bias-field correct a subject's T1w image. */

    publishDir "${params.output_dir}/preprocess", mode: 'copy'

    input:
        path t1w

    output:
        path "sub-${params.subject}_desc-preproc_T1w.nii.gz", emit: preproc_t1w

    script:
    def bet_fi = params.bet_fractional_intensity != null ? params.bet_fractional_intensity : 'None'
    """
    ${params.python_cmd} ${projectDir}/src/nextflow_niwrap/preprocess.py \\
        --t1w "${t1w}" \\
        --output "sub-${params.subject}_desc-preproc_T1w.nii.gz" \\
        ${bet_fi != 'None' ? "--bet-fractional-intensity ${bet_fi}" : ""}
    """
}


process registration_to_template {
    /* Register the preprocessed T1w image to the template space. */

    publishDir "${params.output_dir}/registration", mode: 'copy'

    input:
        path preproc_t1w

    output:
        path "sub-${params.subject}_space-${params.template}_desc-preproc_T1w.nii.gz", emit: xfm_t1w

    script:
    def template_t1w = "${params.data_dir}/templateflow/tpl-${params.template}/tpl-${params.template}_res-01_T1w.nii.gz"
    """
    ${params.python_cmd} ${projectDir}/src/nextflow_niwrap/register.py \\
        --moving "${preproc_t1w}" \\
        --fixed "${template_t1w}" \\
        --output "sub-${params.subject}_space-${params.template}_desc-preproc_T1w.nii.gz"
    """
}


workflow {
    t1w_ch = Channel.fromPath(
        "${params.data_dir}/ds000001/sub-${params.subject}/anat/sub-${params.subject}_T1w.nii.gz"
    )

    anatomical_preprocess(t1w_ch)
        | registration_to_template
}
