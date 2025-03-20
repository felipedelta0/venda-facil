package controllers

import (
	"net/http"
	"strconv"
	"venda-facil/api/models"

	"github.com/gin-gonic/gin"
)

var stocks = []models.Stock{
	{ID: 1, Name: "Produto 1", Quantity: 10},
	{ID: 2, Name: "Produto 2", Quantity: 15},
	{ID: 3, Name: "Produto 3", Quantity: 20},
	{ID: 4, Name: "Produto 4", Quantity: 25},
	{ID: 5, Name: "Produto 5", Quantity: 30},
}

func GetStock(c *gin.Context) {
	c.JSON(http.StatusOK, stocks)
}

func GetStockByID(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	for _, stock := range stocks {
		if stock.ID == id {
			c.JSON(http.StatusOK, stock)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"message": "Produto não encontrado"})
}

func CreateStock(c *gin.Context) {
	var newStock models.Stock
	if err := c.ShouldBindJSON(&newStock); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	stocks = append(stocks, newStock)
	c.JSON(http.StatusCreated, newStock)
}

func UpdateStock(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	var updatedStock models.Stock
	if err := c.ShouldBindJSON(&updatedStock); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	for i, stock := range stocks {
		if stock.ID == id {
			stocks[i] = updatedStock
			c.JSON(http.StatusOK, updatedStock)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"message": "Produto não encontrado"})
}

func DeleteStock(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	for i, stock := range stocks {
		if stock.ID == id {
			stocks = append(stocks[:i], stocks[i+1:]...)
			c.JSON(http.StatusOK, gin.H{"message": "Produto deletado"})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"message": "Produto não encontrado"})
}
