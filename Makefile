.PHONY: all clean

all: data/processed/sales.csv \
		data/processed/weather.csv \
		data/processed/combined.csv \
		data/modelling/train.csv \
		data/modelling/test.csv \
		model/lr_pipe_total_sales.pkl \
		model/lr_pipe_item_A_sales.pkl \
		model/lr_pipe_item_B_sales.pkl \
		model/pr_pipe_orders.pkl \
		results/mae_grouped_total_sales.csv \
		results/trained_coef_total_sales.csv \
		results/lr_plot.pkl \
		results/resid_dist_plot.pkl \
		results/resid_fit_plot.pkl \
		results/mae_grouped_item_A.csv \
		results/trained_coef_item_A.csv \
		results/lr_plot_item_A.pkl \
		results/resid_dist_plot_item_A.pkl \
		results/resid_fit_plot_item_A.pkl \
		results/mae_grouped_item_B.csv \
		results/trained_coef_item_B.csv \
		results/lr_plot_item_B.pkl \
		results/resid_dist_plot_item_B.pkl \
		results/resid_fit_plot_item_B.pkl \
		results/mae_grouped_orders.csv \
		results/trained_coef_orders.csv \
		results/pr_plot_orders.pkl \
		results/resid_dist_plot_orders.pkl \
		results/resid_fit_plot_orders.pkl

# prepare sales.csv 
data/processed/sales.csv: scripts/prepare_sales.csv.py
	python scripts/prepare_sales.csv.py 

# prepare weather.csv
data/processed/weather.csv: scripts/prepare_weather.csv.py
	python scripts/prepare_weather.csv.py 

# prepare combined.csv, train.csv, test.csv 
data/processed/combined.csv data/modelling/train.csv data/modelling/test.csv: scripts/prepare_combined.csv.py data/processed/sales.csv data/processed/weather.csv
	python scripts/prepare_combined.csv.py

# train total sales prediction pipeline
model/lr_pipe_total_sales.pkl: scripts/train_model_total_sales.py
	python scripts/train_model_total_sales.py

# train item_A prediction pipeline
model/lr_pipe_item_A_sales.pkl: scripts/train_model_item_A.py 
	python scripts/train_model_item_A.py 

# train item_B prediction pipeline
model/lr_pipe_item_B_sales.pkl: scripts/train_model_item_B.py 
	python scripts/train_model_item_B.py 

# train order volume prediction pipeline
model/pr_pipe_orders.pkl: scripts/train_model_orders.py
	python scripts/train_model_orders.py

# generate model results - total sales
results/mae_grouped_total_sales.csv results/trained_coef_total_sales.csv results/lr_plot.pkl results/resid_dist_plot.pkl results/resid_fit_plot.pkl: scripts/get_model_results_total.py
	python scripts/get_model_results_total.py

# generate model results - item A sales 
results/mae_grouped_item_A.csv results/trained_coef_item_A.csv results/lr_plot_item_A.pkl results/resid_dist_plot_item_A.pkl results/resid_fit_plot_item_A.pkl: scripts/get_model_results_A.py
	python scripts/get_model_results_A.py

# generate model results - item B sales 
results/mae_grouped_item_B.csv results/trained_coef_item_B.csv results/lr_plot_item_B.pkl results/resid_dist_plot_item_B.pkl results/resid_fit_plot_item_B.pkl: scripts/get_model_results_B.py
	python scripts/get_model_results_B.py

# generate model results - orders
results/mae_grouped_orders.csv results/trained_coef_orders.csv results/pr_plot_orders.pkl results/resid_dist_plot_orders.pkl results/resid_fit_plot_orders.pkl: scripts/get_model_results_orders.py
	python scripts/get_model_results_orders.py

clean:
	rm -f data/processed/sales.csv \
		  data/processed/weather.csv \
		  data/processed/combined.csv \
		  data/modelling/train.csv \
		  data/modelling/test.csv \
		  model/lr_pipe_total_sales.pkl \
		  model/lr_pipe_item_A_sales.pkl \
		  model/lr_pipe_item_B_sales.pkl \
		  model/pr_pipe_orders.pkl \
		  results/mae_grouped_total_sales.csv \
		  results/trained_coef_total_sales.csv \
		  results/lr_plot.pkl \
		  results/resid_dist_plot.pkl \
		  results/resid_fit_plot.pkl \
		  results/mae_grouped_item_A.csv \
		  results/trained_coef_item_A.csv \
		  results/lr_plot_item_A.pkl \
		  results/resid_dist_plot_item_A.pkl \
		  results/resid_fit_plot_item_A.pkl \
		  results/mae_grouped_item_B.csv \
		  results/trained_coef_item_B.csv \
		  results/lr_plot_item_B.pkl \
		  results/resid_dist_plot_item_B.pkl \
		  results/resid_fit_plot_item_B.pkl \
		  results/mae_grouped_orders.csv \
		  results/trained_coef_orders.csv \
		  results/pr_plot_orders.pkl \
		  results/resid_dist_plot_orders.pkl \
		  results/resid_fit_plot_orders.pkl

