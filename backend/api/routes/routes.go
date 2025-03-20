package routes

import (
	"venda-facil/api/controllers"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(router *gin.Engine) {
	router.GET("/ping", controllers.Ping)

	router.GET("/stock", controllers.GetStock)
	router.GET("/stocks/:id", controllers.GetStockByID)
	router.POST("/stocks", controllers.CreateStock)
	router.PUT("/stocks/:id", controllers.UpdateStock)
	router.DELETE("/stocks/:id", controllers.DeleteStock)
}
