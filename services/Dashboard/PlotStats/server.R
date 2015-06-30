## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu
## 6/24/2015


# server.R
source('helpers.R')
library(shiny)
library(googleVis)


shinyServer(function(input, output,session) {

  
  output$UserList <- renderUI({  
    
    checkboxGroupInput("checkGroup", 
                       label = h5("Usernames:"), 
                       choices = userNames ,
                       selected = NULL)#c("dwkimiti@gmail.com","corwaal@gmail.com"))
    
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
  

  ###########################
  
  output$MonthList <- renderUI({  
    
    checkboxGroupInput("checkMonthGroup", 
                       label = h5("Months:"), 
                       choices = months ,
                       selected = NULL)
    
  })
  
  observe({
    if (input$selectAllMonth){
      
      updateCheckboxGroupInput( session, "checkMonthGroup", 
                                choices = months ,
                                selected = months) 
    }
  })
  
  observe({
    if(input$deselectAllMonth)
    {
      updateCheckboxGroupInput( session, "checkMonthGroup", 
                                choices = months ,
                                selected = NULL  ) 
    }
    
  })
  


  ###########################

  output$chart1 <- renderGvis({
  
    shiny::validate(need(input$checkGroup , 'Check at least one userName!' ))    
    shiny::validate(need(input$checkMonthGroup , 'Check at least one date!' ))  

    UserData<-getUserData(input$checkGroup,input$checkMonthGroup)
    
    shiny::validate(need(UserData , 'No data to display!' ))  
    #UserData<-getTransposeData(input$checkGroup)
    
    gvisColumnChart(UserData)
#       gvisAnnotationChart(UserData, datevar="time",
#                           numvar="x", idvar="user",
#                           titlevar="", annotationvar="user",
#                           chartid="AnnotationChart",
#                           options=list(
#                             width=1000, height=550,
#                             displayAnnotationsFilter = TRUE,
#                              displayExactValues =TRUE,
# #                             scaleColumns='[0]',
#                             scaleType='allmaximized',
#                             fill=10, displayExactValues=TRUE)
#       )    

  })
}) 
