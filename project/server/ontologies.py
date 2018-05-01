
from isatools.model import (
    Comment,
    Investigation,
    OntologySource,
    OntologyAnnotation,
)


DATA_TYPES = [
    dict(
        name='Simulation', type=OntologyAnnotation(term='Simulation'),
        short_display='Simulated', long_display='Simulated Data'
    ),
    dict(
        name='Experimental', type=OntologyAnnotation(term='Experimental'),
        short_display='Experimental', long_display='Experimental Data'
    ),
    dict(
        name='Literature', type=OntologyAnnotation(term='Literature'),
        short_display='Literature', long_display='Literature Data'
    ),
]


ONTOLOGY_ANNOTATIONS = [
    dict(
        name='NMR', type=OntologyAnnotation(term='NMR'),
        short_display='NMR', long_display='Nuclear Magnetic Resonance'
    ),
    dict(
        name='27_Al', type=OntologyAnnotation(term='27 Al'),
        short_display='27 Al', long_display='27 Aluminum'
    ),

    # OntologyAnnotation(term='Percent Purity by Weight'),
    # OntologyAnnotation(term='Celsius'),
    # OntologyAnnotation(term='NMR Reference Compound'),
    # OntologyAnnotation(term='Hydroxide'),
    # OntologyAnnotation(term='Aluminum'),
    # OntologyAnnotation(term='Sodium'),
    # OntologyAnnotation(term='Caesium'),
    # OntologyAnnotation(term='Lithium'),
    # OntologyAnnotation(term='Potassium'),
]

UNIT_FACTORS = [
    dict(
        name='Molarity', type=OntologyAnnotation(term='Molarity'),
        short_display='M', long_display='Molarity'
    ),
    dict(
        name='wt_purity', type=OntologyAnnotation(term='Percent Purity by Weight'),
        short_display=u'wt %', long_display='Percent Purity by Weight'
    ),
    dict(
        name='Celsius', type=OntologyAnnotation(term='Celsius'),
        short_display='C', long_display='Degrees Celsius'
    ),
]


FACTOR_FACTORS = [
    dict(
        name='counter_ion', type=OntologyAnnotation(term='Counter Ion'),
        short_display='M+', long_display='Counter Ion',
        factors=['Na+', 'Li+', 'Cs+', 'K+']
    ),
]

# STRING_FACTORS
