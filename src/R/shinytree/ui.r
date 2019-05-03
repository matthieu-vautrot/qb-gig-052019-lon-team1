# Rely on the 'WorldPhones' dataset in the datasets
# package (which generally comes preloaded).
library(datasets)
library(shinythemes)

# Use a fluid Bootstrap layout
fluidPage(theme = shinytheme("darkly"),titlePanel(title=div(img(src="Picture1.png")),"QB GIG - Team 1"),

  # Give the page a title

  # Generate a row with a sidebar
  sidebarLayout(

    # Define the sidebar with one input
    sidebarPanel(
      uiOutput("choose_target"),
      uiOutput("choose_producer"),
      uiOutput("choose_molecule"),

      # uiOutput("choose_brand"),
      sliderInput("tree_cp", "Complexity parameter:",
                  min = 0.0005, max = 0.1, value = 0.05, step = 0.001
      ),
      uiOutput("choose_top_mol"),
      uiOutput("choose_columns")
    ),

    mainPanel(
      plotOutput("cartPlot"),
      textInput(inputId = "pict_name", label = "picture file name" ,value = ""),
      textInput(inputId = "comment", label = "picture comment", value = ""),
      actionButton("save_fig", "Save tree picture")

    )

  )
)
