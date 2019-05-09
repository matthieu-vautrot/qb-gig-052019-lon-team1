
# To fix by pointing to master table
data_src = "/Users/matthew_aaron_cooke/qb-gig-052019-lon-team1/data/05_model_input/model_input.csv"
data_src = "/Users/matthieu_vautrot/work/gig-2019-local/qb-gig-052019-lon-team1/src/R/shinytree/data/master.csv"

source("master_col.r")
io_path = "/home/matthieu_v/tree_out/"

options(shiny.host = "0.0.0.0")
options(shiny.port = 8788)

df = read.table(file = data_src, sep = ',', header = TRUE)

get_fea <-function(df)
{
  return(fea_col)
}

get_tg_col <- function(l){
  return(tg_col)
}
