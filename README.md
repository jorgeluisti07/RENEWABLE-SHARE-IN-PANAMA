# Renewable Share in Panama

Hourly analysis of Panama's electricity system for 2025: combines system demand with Solar, Wind, and Hydro generation to calculate **Net Load** and **Renewables Share** for every hour of the year.

## Data

| File | Contents |
|---|---|
| `DEM2025.csv` | Hourly system electricity demand (MW) for 2025 — one row per day, columns `H1`-`H24` |
| `solar_eolica_hidro_horario_2025.csv` | Hourly Solar, Wind, and Hydro generation (MW) for 2025 — one row per hour, columns `solar_mw_real`, `eolica_mw_real`, `hidro_mw_real` |
| `RENEWABLES SHARE IN PANAMA.ipynb` | The analysis notebook |

## Key metrics

**Net Load (MW)** — the portion of demand not covered by renewables:

```
Net Load = Demand − (Solar + Wind + Hydro), floored at 0
```

This is the electricity demand that has to be met by other sources — in Panama's case, mainly thermal (fossil-fuel) generation. A smaller net load means more of the system's demand is being met by renewables, and less thermal generation is needed to keep supply secure.

**Renewables Share (%)** — how much of demand renewables are covering, per hour:

```
Renewables Share = (Solar + Wind + Hydro) / Demand × 100, capped at 100%
```

Both metrics fluctuate hour to hour because demand and each generation source move independently — solar drops to zero overnight, wind output is intermittent, and hydro depends on reservoir/river conditions. Together they track how much of Panama's electricity is being met by renewables versus thermal generation, which is a core metric for following decarbonization progress: a falling net load and a rising renewables share both mean less reliance on fossil-fuel units.

## Notes on the data

- `DEM2025.csv` contains one invalid row (`02/29/2025` — 2025 is not a leap year); it's dropped during processing, leaving a clean 365-day year.
- The `H1`-`H24` demand columns use an hour-ending convention (`H1` = 00:00–01:00, ..., `H24` = 23:00–00:00 the next day), matching the timestamps in the generation file.
- The generation file is sometimes downloaded with a `.xls` extension even though its contents are plain CSV text rename it, or adjust the `pd.read_csv` filename in the notebook to match whatever you actually have on disk.

## Running it

Open `RENEWABLES SHARE IN PANAMA.ipynb` and run all cells top to bottom. It loads both CSVs, aligns them on an hourly datetime index, and produces:

- Hourly demand vs. Solar/Wind/Hydro generation plot
- Net Load plot
- Net Load vs. Demand comparison
- Renewables Share (%) over the year
