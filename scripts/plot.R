library(ggplot2)
library(dplyr)

### surSeg ###

surSeg_results <- read.csv('../surSeg_results.txt', header = T, sep = ' ')
surSeg_results$Select_size <- as.factor(surSeg_results$Select_size)
surSeg_results$Value <- as.numeric(surSeg_results$Value)

subset(surSeg_results, Metric == 'f1' & Size == '50') %>% 
  ggplot(aes(Select_size, Value, group = Size, color = Size)) +
  geom_line() +
  geom_point()
  #  scale_shape_manual(values = c(3, 16, 3, 16)) +
#  scale_color_manual(values = c("steelblue",  "mediumpurple4")) +  
  facet_wrap( ~ Language) +
  scale_x_continuous(breaks=seq(0, 1200, 100)) +
  #  scale_y_continuous(breaks=seq(0, 1300, 100)) +
  theme_classic() + 
  theme(text = element_text(size=18)) + #, family="Times"
  theme(legend.position="top") +
  xlab("selection size") + 
  ylab("F1") + 
  guides(color = guide_legend(nrow = 2)) + 
  theme(legend.title = element_blank()) 