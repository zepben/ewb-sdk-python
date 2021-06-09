from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["TransformerTest"]


class TransformerTest(IdentifiedObject):
    """
    Test result for transformer ends, such as short-circuit, open-circuit (excitation) or no-load test.
    """

    base_power: int = 0
    """
    Base power at which the tests are conducted, usually equal to the ratedS of one of the involved transformer ends in VA.
    """

    temperature: float = 0.0
    """
    Temperature at which the test is conducted in degrees Celsius.
    """
