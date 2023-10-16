from zepben.evolve import TablePowerElectronicsUnit

__all__ = ["TableEvChargingUnits"]


class TableEvChargingUnits(TablePowerElectronicsUnit):

    def name(self) -> str:
        return "ev_charging_units"
