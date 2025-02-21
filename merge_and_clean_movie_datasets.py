import pandas as pd
import re


# 1. Load Data
tmdb_file = "C:/Users/aabgk/Downloads/TMDB_movie_dataset_v11.csv"
metacritic_file = "C:/Users/aabgk/Downloads/metacritic-reviews.csv"
letterboxd_file = "C:/Users/aabgk/Downloads/letterboxd-reviews.csv"

tmdb_df = pd.read_csv(tmdb_file, encoding="utf-8")
metacritic_df = pd.read_csv(metacritic_file, encoding="ISO-8859-1", on_bad_lines='skip')
letterboxd_df = pd.read_csv(letterboxd_file, encoding="ISO-8859-1")

tmdb_df.rename(columns={'title': 'Movie name'}, inplace=True)

merged_df = tmdb_df.merge(metacritic_df, on="Movie name", how="inner")
merged_df = merged_df.merge(letterboxd_df, on="Movie name", how="inner")
merged_df = merged_df.drop_duplicates()

merged_file = "C:/Users/aabgk/Downloads/merged_df.csv"
merged_df.to_csv(merged_file, index=False, encoding="utf-8")

print(f"Total Records (Rows): {merged_df.shape[0]}")
print(f"Total Columns: {merged_df.shape[1]}\n")
print("Column Headers:", list(merged_df.columns), "\n")
print(merged_df.head())


# Explore
print(merged_df.info())
print("\n")

print(merged_df.head())
print("\n")

print(merged_df.describe())
print("\n")

print(merged_df.isna().sum())
print("\n")



duplicates = merged_df.duplicated().sum()
print(f"5. Duplicate Rows Remaining: {duplicates}\n")

if 'status' in merged_df.columns:
    print("Unique 'status' Values:", merged_df['status'].unique())
    print()

if 'adult' in merged_df.columns:
    print("Unique 'adult' Values:", merged_df['adult'].unique())
    print()



def parse_star_rating(star_str):
    if not isinstance(star_str, str):
        return None
    star_str = star_str.strip()
    full_stars = star_str.count("â??")
    half_star = 0.5 if "â½" in star_str else 0.0
    return full_stars + half_star

merged_df["Rating_y_cleaned"] = merged_df["Rating_y"].apply(parse_star_rating)

merged_df.drop("Rating_y", axis=1, inplace=True)

# Convert dates
date_cols = ["Release Date", "Review date"]
for col in date_cols:
    if col in merged_df.columns:
        merged_df[col] = pd.to_datetime(merged_df[col], errors="coerce")



# Drop cols with many missing non-numerical values, ids, repeat columns
cols_to_drop = [
    "homepage", "backdrop_path", "tagline", "poster_path",
    "release_date", "imdb_id", "keywords"
]
merged_df.drop(columns=[c for c in cols_to_drop if c in merged_df.columns],
               inplace=True,
               errors="ignore")



# Concat digits for like and comment count
def concatenate_all_digits(text):
    if pd.isna(text):
        return None
    digits = re.findall(r'\d+', str(text))
    if not digits:
        return None
    concatenated = "".join(digits)  # e.g. ["6", "6", "08"] -> "6608"
    return int(concatenated)

if "Like count" in merged_df.columns:
    merged_df["Like count"] = merged_df["Like count"].apply(concatenate_all_digits)

if "Comment count" in merged_df.columns:
    merged_df["Comment count"] = merged_df["Comment count"].apply(concatenate_all_digits)


# Check and save
print(merged_df.info())
print(merged_df.isna().sum())
print(merged_df.head())

cleaned_file = "C:/Users/aabgk/Downloads/merged_df_cleaned.csv"
merged_df.to_csv(cleaned_file, index=False, encoding="utf-8")
print(f" saved to: {cleaned_file}")