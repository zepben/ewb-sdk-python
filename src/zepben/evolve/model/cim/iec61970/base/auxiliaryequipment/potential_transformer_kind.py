from enum import Enum

__all__ = ["PotentialTransformerKind"]


class PotentialTransformerKind(Enum):
    """
    The construction kind of the potential transformer.
    """

    UNKNOWN = 0
    """The construction type of the potential transformer is unknown."""

    inductive = 1
    """The potential transformer is using induction coils to create secondary voltage."""

    capacitiveCoupling = 2
    """The potential transformer is using capacitive coupling to create secondary voltage."""

    @property
    def short_name(self):
        return str(self)[25:]
