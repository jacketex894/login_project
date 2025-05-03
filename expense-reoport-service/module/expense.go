package models

import "time"

type Expense struct {
    Title     string    `json:"title"`
    Amount    float64   `json:"amount"`
	Quantity  int       `json:"quantity"`
	Comment   string    `json:"comment"`
    Date      time.Time `json:"date"`
}