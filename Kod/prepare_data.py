#Read trains.parquet
import polars as pl

trains = pl.read_parquet("Data/Laboration 3/trains.parquet")

# Konvertera 'Weekday' till enum (categorical)
if "Weekday" in trains.columns and not isinstance(trains["Weekday"].dtype, pl.Enum):
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    trains = trains.with_columns([
        pl.col("Weekday").cast(pl.Enum(weekdays))
    ])

# Konvertera 'Hour' till enum (categorical)
if "Hour" in trains.columns and not isinstance(trains["Hour"].dtype, pl.Enum):
    hour_order = [str(h) for h in range(24)]
    trains = trains.with_columns([
        pl.col("Hour").cast(pl.Utf8).cast(pl.Enum(hour_order))
    ])

trains = (
    trains
    .drop_nulls(["PlannedDwellTime", "ActualDwellTime"])
    .filter((pl.col("PlannedDwellTime") >= 0) & (pl.col("ActualDwellTime") >= 0)) #tar bort orimliga värden
    .filter((pl.col("PlannedDwellTime") <= 15) & (pl.col("ActualDwellTime") <= 60)) #tar bort extrema värden
)

# read reasons as a dictinary {code: description}
reasons = pl.read_parquet("Data/Laboration 3/reasons.parquet")
reasons_dict = {
    row["Code"]: row["Level3Description"]
    for row in reasons.iter_rows(named=True)
}
# add reasons_dict to trains
trains = trains.with_columns(
    pl.col("DeviationCodes")
    .map_elements(
        lambda codes: (
            []
            if codes is None
            else [reasons_dict[code] for code in codes if code in reasons_dict]
        ),
        return_dtype=pl.List(pl.String),
    )
    .alias("Deviations")
)


# Write back to parquet
trains.write_parquet("Data/Laboration 3/trains.parquet")