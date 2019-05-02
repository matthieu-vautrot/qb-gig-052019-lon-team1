## NEW APP

# guide to install rattle properly on mac
# https://gist.github.com/zhiyzuo/a489ffdcc5da87f28f8589a55aa206dd

install_n_load <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg))
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}
install_n_load_from_git <- function(pkg){
  splitted <- lapply(X = strsplit(x=pkg, '/'), FUN= function(x){x[2]})
  splitted <- c(do.call("cbind", splitted))
  new.pkg <- pkg[!(splitted %in% installed.packages()[, "Package"])]
  if (length(new.pkg)){
    print(new.pkg)
    install_github(new.pkg)
  }
  sapply(X=splitted, FUN = require, character.only = TRUE)
}

packages <- c('shiny', 'rpart', 'rpart.plot', 'data.table')

install_n_load(packages)

ifelse_ <- function(bool, x, y) if(bool) x else y


