# server.R
source('helpers.R')
library(shiny)
library(googleVis)


shinyServer(function(input, output,session) {
  first<<- TRUE
  
  
##https://landpotential.shinyapps.io/LandCoverCharts/?userName=dwkimiti@gmail.com

  output$PlotNames <- renderUI({
    
    searchStr = parseQueryString(session$clientData$url_search)
#     print(searchStr["userName"])
    shiny::validate(
      need("userName" %in% names(searchStr) ,'No data to display!')
      ,
      need(searchStr["userName"] != "" ,'No data to display!')
    )
    
    prepareData(searchStr["userName"])
    
    checkboxGroupInput("checkGroup", 
                       label = h5("Plot list:"), 
                       choices = plotNames ,
                       selected = plotNames[1])
  })
  

  observe({
    if (input$selectAll){
      
      updateCheckboxGroupInput( session, "checkGroup", 
                                choices = plotNames ,
                                selected = plotNames) 
      first <<- FALSE
    }
  })
    
    observe({
    if(input$deselectAll)
      {
       updateCheckboxGroupInput( session, "checkGroup", 
                                 choices = plotNames ,
                                 selected = NULL  ) 
      }

  })
  

  
  output$chart1 <- renderGvis({
    
    shiny::validate(need(input$checkGroup, 'Check at least one plot!' ))    
    
    
    switch(input$charts, 
           "Height class multi bar chart" = heightChart(),
           "Gap percentage chart" = gapChart(),
           "Cover/Bare ground chart" = coverageChart(), 
           "Species Density chart"= speciesChart(),
           "Plant Cover/Composition multi bar chart" = plantCoverChart(),
           "Foliar Cover chart" = foliarChart(),
           "test combined chart" = testChart()
    )
  })
  
  output$summary<- renderText ({
   
    switch(input$charts, 
           "Height class multi bar chart" = "This chart displays different height classes for each plot.",
           "Gap percentage chart" = "This chart displays different Gap types for each plot.",
           "Cover/Bare ground chart" = "This chart shows Bare ground and cover percentage for each plot.", 
           "Species Density chart"= "Species Density is represented in this chart.",
           "Plant Cover/Composition multi bar chart" = "this is Plant Cover/Composition multi bar chart",
           "Foliar Cover chart" = "this is Foliar Cover chart",
           "test combined chart" = "this is test combined chart"
    )   
    
  }) 
  
  heightChart <- function() {
    
    heightData<-getHeight(input$checkGroup)
    p <- gvisComboChart(heightData, xvar = "plotNames" , yvar = c("<10cm", "10-50cm", "50cm-1m", "1-2m", "2-3m", ">3m"), options = list(seriesType = "bars",                                                                                       title = "Height class", series = ""))
    
  }
  
  plantCoverChart<- function(){
    plantCoverData<-getPlantCover(input$checkGroup)
    p <- gvisComboChart(plantCoverData, xvar = "plotNames", yvar = c("trees_total","shrubs_total",  "sub_shrubs_total",  "perennial_grasses_total",  "annuals_total"), options = list(seriesType = "bars", 
                                                                                            title = "Plant Cover class", series = ""))
    
  }
  
  gapChart <- function() {
    data<-getGap(input$checkGroup)
    p <- gvisComboChart(data, xvar = "plotNames", yvar = c("Canopy gap%", "Basal gap %") , options = list(seriesType = "bars", 
                                                                                                          title = "Gap percentage", series = ""))
    
  }
  coverageChart <- function() {
    data<-getCoverage(input$checkGroup)
    p <- gvisComboChart(data, xvar = "plotNames", yvar = c("Bare Ground%", "Cover%") , options = list(seriesType = "bars", 
                                                                                                          title = "Cover/Bare ground percentage", series = "", colors="[ '#FF0000' , '#009000']"))
    
  }
  speciesChart <- function() {
    data<-getSpecies(input$checkGroup)
    p <- gvisComboChart(data, xvar = "plotNames", yvar = c("Species 1", 
                                                           "Species 2") , options = list(seriesType = "bars", 
                                                                                         title = "Species", series = ""))
    
  }
  
  foliarChart <- function() {
    data<-getFoliar(input$checkGroup)
    p <- gvisColumnChart(data,yvar = "Foliar Cover" , xvar = "plotNames", options =list(title = "Foliar cover percentage"))
#     data<-data[c(2,1)]
#    Gauge <-  gvisGauge(data,labelvar  = "plotNames", numvar = "Foliar Cover", options=list(min=0, max=100, greenFrom=66,
#                                                     greenTo=100, yellowFrom=33, yellowTo=66,
#                                                     redFrom=0, redTo=33, width=700, height=500))
#    
   
  }
  
  
  testChart<-function(){
    
    testData<-merge(getGap(input$checkGroup),getFoliar(input$checkGroup),by = "plotNames")
    p <- gvisBubbleChart(testData, idvar="plotNames", 
                              xvar="Canopy gap%", yvar="Basal gap %",
                               sizevar="Foliar Cover",
                         options=list(
                           hAxis='{minValue:0, maxValue:110, title:"Canopy Gap"}',
                           vAxis= '{minValue:0, maxValue:110, title: "Basal Gap"}',
                           colorAxis='{minValue:0, legend:"Foliar Cover"}'
                           ))
  }
  
}) 
