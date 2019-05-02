
data_src = "data/master.csv"
source("data/master_col.r")

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
