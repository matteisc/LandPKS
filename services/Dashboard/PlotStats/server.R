## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(shiny)
library(googleVis)

server<-function(input, output,session) {

  
  output$UserList <- renderUI({  
    
    div(style='height:500px;  overflow: scroll'  
            ,checkboxGroupInput("checkGroup", 
                               label = h5("Usernames:"), 
                               choices = userNames ,
                               selected = userNames))      
  })
  
  observe({
    if (input$selectAll){
      
      updateCheckboxGroupInput( session, "checkGroup", 
                                choices = userNames ,
                                selected = userNames) 
    }
  })
  
  observe({
    if(input$deselectAll)
    {
      updateCheckboxGroupInput( session, "checkGroup", 
                                choices = userNames ,
                                selected = NULL  ) 
    }
    
  })
  
  
  #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  output$OrgList <- renderUI({  
    
    div(style='height:500px;  overflow: scroll'  
        ,checkboxGroupInput("checkGroupOrg", 
                            label = h5("Organizations:"), 
                            choices = orgNames ,
                            selected = orgNames))      
  })
  
  observe({
    if (input$selectAllOrg){
      
      updateCheckboxGroupInput( session, "checkGroupOrg", 
                                choices = orgNames ,
                                selected = orgNames) 
    }
  })
  
  observe({
    if(input$deselectAllOrg)
    {
      updateCheckboxGroupInput( session, "checkGroupOrg", 
                                choices = orgNames ,
                                selected = NULL  ) 
    }
    
  })
  

  ###########################

  selectedPlot <- reactive({
    shiny::validate(need(input$checkGroup , 'Check at least one userName!' ))     
    shiny::validate(need(input$dates[2] >= input$dates[1], "end date should be after start date"))
    
    UserData<-getUserData(input$checkGroup,input$dates,input$count)
    
    shiny::validate(need(UserData , 'No data to display!' ))  
    UserData
    
  })
  
  output$chart1 <- renderGvis({
   
    gvisColumnChart(selectedPlot())

  })
  
  
    output$stats <- renderText({
      selectedPlot()
      updateStats()
      })
  
  #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  selectedPlotOrg <- reactive({
    shiny::validate(need(input$checkGroupOrg , 'Check at least one organization!' ))     
    shiny::validate(need(input$dates[2] >= input$dates[1], "end date should be after start date"))
    
    OrgData<-getOrgData(input$checkGroupOrg,input$datesOrg,input$countOrg)
    
    shiny::validate(need(OrgData , 'No data to display!' ))  
    OrgData
    
  })
  
  output$chartOrg <- renderGvis({
    
    gvisColumnChart(selectedPlotOrg())
    
  })
  
  
  output$orgStats <- renderText({
    selectedPlotOrg()
    updateOrgStats()
  })
  
  ####################################
  output$tbl <- renderDataTable(json_data[, -which(names(json_data) %in% c("value","shortdate"))], options = list(pageLength = 10))
  
  
}
