.PHONY: all clean

all: data/processed/sales.csv data/processed/weather.csv data/processed/combined.csv model/lr_pipe_total_sales.pkl results/mae_grouped_total_sales.csv results/trained_coef_total_sales.csv

# prepare sales.csv 
data/processed/sales.csv: scripts/prepare_sales.csv.py
	python scripts/prepare_sales.csv.py 

# prepare weather.csv
data/processed/weather.csv: scripts/prepare_weather.csv.py
	python scripts/prepare_weather.csv.py 

# prepare combined.csv, train.csv, test.csv 
data/processed/combined.csv data/modelling/train.csv data/modelling/test.csv: scripts/prepare_combined.csv.py data/processed/sales.csv data/processed/weather.csv
	python scripts/prepare_combined.csv.py

# train pipeline
model/lr_pipe_total_sales.pkl: scripts/train_model.py
	python scripts/train_model.py 

# generate model results
results/mae_grouped_total_sales.csv results/trained_coef_total_sales.csv results/lr_plot.pkl results/resid_dist_plot.pkl results/resid_fit_plot.pkl results/resid_plot.pkl: scripts/get_model_results.py
	python scripts/get_model_results.py

clean:
	rm -f data/processed/sales.csv \
		  data/processed/weather.csv \
		  data/processed/combined.csv \
		  data/modelling/train.csv \
		  data/modelling/test.csv \
		  model/lr_pipe_total_sales.pkl \
		  results/mae_grouped_total_sales.csv \
		  results/trained_coef_total_sales.csv \
		  results/lr_plot.pkl \
		  results/resid_dist_plot.pkl \
		  results/resid_fit_plot.pkl \
		  results/resid_plot.pkl