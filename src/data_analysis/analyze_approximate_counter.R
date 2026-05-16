library(dplyr)
library(ggplot2)

# loading data to analyze
csv_folder <- "results/dynamic_counter"
csv_files <- list.files(csv_folder, pattern = "^approximate_counter_run_.*\\.csv$", full.names = TRUE)

load_csv <- function(file) {
  df <- read.csv(file, stringsAsFactors = FALSE)
  return(df)
}

csv_list <- lapply(csv_files, load_csv)

for(i in seq_along(csv_list)) {
  csv_list[[i]]$run <- i
}

all_data <- bind_rows(csv_list)

# calculating some sample statistics
summary_stats <- all_data %>%
  group_by(Town) %>%
  summarise(
    mean_count = as.numeric(mean(RawCount)),
    median_count = as.numeric(median(RawCount)),
    sd_count = as.numeric(sd(RawCount)),
    .groups = 'drop'
  ) %>%
  arrange(desc(mean_count))

# since we count with p=1/8, we should multiply mean by 8
p <- 1/8
summary_stats <- summary_stats %>%
  mutate(
    scaled_mean = as.numeric(mean_count / p),
    scaled_median = as.numeric(median_count / p),
    scaled_sd = as.numeric(sd_count / p)
  )

print(head(summary_stats, 5))

# this part serves to calculate town occurence, since we could miss rare towns
town_presence <- lapply(csv_list, function(df) {
  unique(df$Town)
})


all_towns <- unlist(town_presence)
town_counts <- as.data.frame(table(all_towns)) # counting the occurrences
colnames(town_counts) <- c("Town", "NumRuns")

town_counts <- town_counts %>% arrange(desc(NumRuns)) # sorting descendingly

# histogram: how many times was each town spotted?
ggplot(town_counts, aes(x = NumRuns)) +
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  labs(
    title = "Distribution of Town Appearances Across Runs",
    x = "Number of runs town was counted",
    y = "Number of towns"
  ) +
  theme_minimal()


# percentage of cities that were spotted 100, 200, 300, ... 1000 times
thresholds <- seq(100, 1000, by = 100)
percentages <- sapply(thresholds, function(t) {
  mean(town_counts$NumRuns >= t) * 100
})

threshold_df <- data.frame(
  Threshold = thresholds,
  PercentOfTowns = percentages
)

print(threshold_df)
