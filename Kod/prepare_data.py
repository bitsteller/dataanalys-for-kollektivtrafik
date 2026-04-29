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

# Write back to parquet
trains.write_parquet("Data/Laboration 3/trains.parquet")