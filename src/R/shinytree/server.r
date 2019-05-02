source("library.R")
source("global.R")

fg_top_ten <- TRUE

cart <- NULL
nrow <- NULL
rmse <- NULL
rsq  <- NULL

# prework project specific on features filtering
# split by a category - if sub tree needs to happen
# e.g. split by molecule category  - producer ..
# in server function
# output$choose_producer <- renderUI({
#   selectInput("producer", "producers",producer)
# })

df

# Define a server for the Shiny app
function(input, output, session) {

  output$choose_target <- renderUI({
    selectInput("target", "targets", tg_cols)
  })

   output$choose_columns <- renderUI({
     # If missing input, return to avoid error later in function
     if(is.null(df)){
        df <- data
     }

     # Create the checkboxes and select them all by default
     checkboxGroupInput("columns", "Choose columns",
                        choices  = fea_col,
                        selected = fea_col)
   })

   sliderValues <- reactive({
     return(input$tree_cp)})

   output$cartPlot <- renderPlot({
     # bit of logging info
     print(Sys.time())

     df_tree = df
     # split tree by catg if necessary

     tg_col = input$target

     fit_formula <- formula(paste(c(paste(tg_col, "~"),paste(input$columns, collapse='+')),sep='~'))

     cart <<- rpart(fit_formula,data=df_tree, method = 'anova', control = rpart.control(cp = sliderValues()))

     # calculate some tree perf indicators, r2 and RMSE
     nrow <<- nrow(df_tree)

     predictions <- predict(cart, df_tree[input$columns])
     sstot = sum( (df_tree[tg_col] - lapply(df_tree[tg_col], mean, na.rm = TRUE))^2 )
     ssres = sum((df_tree[tg_col] - predictions)^2)

     rmse <<- sqrt(ssres/nrow)
     rsq <<- 1- ssres/sstot
     print(head(predictions))
     print(head(df_tree[tg_col]))
     print(df_tree[tg_col] - predictions)
     print(ssres)
     print(nrow)

     rpart.plot(cart
                , main = paste('Features impact on', tg_col, '(', nrow , 'rows ) -')
                , extra = 101
                , sub = paste('RMSE:', round(rmse, 2), 'R^2:', round(rsq, 4))
     )

   })
   observeEvent(input$save_fig, {
     plot_dir  = paste(io_path, io_title)


     if(input$pict_name != ''){
      filename = paste("ahh", gsub(" ", "_", input$pict_name) , sep = '_')
     }
     else{
       filename = paste("ahh", sep = '_')
     }
     print(filename)
     filename <- paste(plot_dir, filename, sep = '/')
     print(filename)
     png(filename = paste(filename, '.png', sep = ''))
     rpart.plot(cart
                , main = paste('Main Title', '(', nrow, 'rows ) -', "ahh")
                , extra = 101
                , sub = paste('RMSE:', round(rmse, 2), 'R^2:', round(rsq, 4))
     )
     dev.off()
     write(input$comment, file = paste(filename, '.md', sep = ''))
   })
}
