library(dplyr)
library(ggplot2)

# loading the data to serve as baseline
exact_counter <- read.csv("results/exact_counter/exact_counter.csv")

exact_top5 <- exact_counter %>% # Select the top 5 towns by count
  arrange(desc(Count)) %>%
  slice_head(n = 5)

exact_top5_items <- exact_top5$Town

memory_usage <- read.csv("results/space_saving_counter/space_saving_memory_usage.csv")

# Plot memory usage vs k
baseline_kb <- 258704 / 1024
ggplot(memory_usage, aes(x = k, y = memory_bytes /1024)) +  # convert to KB
  geom_line(color = "blue") +
  geom_hline(yintercept = baseline_kb, linetype = "dashed", color = "red") +
  labs(title = "Memory Usage of Space-Saving Counter",
       x = "Number of Counters (k)",
       y = "Memory Usage (KB)") +
  theme_minimal()

# plot frequency of top-5 from the baseline model, compared to space-saving
k_values <- seq(5, 2200, 5)
top5_hits <- data.frame(k = k_values, Hits = NA_integer_)

for (i in seq_along(k_values)) {
  k <- k_values[i]
  path <- sprintf("results/space_saving_counter/space_saving_top5_%d.csv", k)
  
  if (file.exists(path)) {
    ss_top5 <- read.csv(path)
    hits <- sum(ss_top5$Town %in% exact_top5_items) # how many exact top 5 towns are in this top 5?
    top5_hits$Hits[i] <- hits
  } else {
    top5_hits$Hits[i] <- NA
  }
}

ggplot(top5_hits, aes(x = k, y = Hits)) + # Line plot showing number of exact top 5 towns captured in Space-Saving top 5
  geom_line(color = "red") +
  scale_y_continuous(breaks = 0:5) +
  labs(title = "Top 5 Exact Towns Captured in Space-Saving Top 5",
       x = "Number of Counters (k)",
       y = "Number of Exact Top 5 Towns Found") +
  theme_minimal()

hits_eq_1 <- top5_hits %>% # here we can just see for which values did it achieve specific accuracy
  filter(Hits == 5)

print(hits_eq_1)
