
from flask import Blueprint, request, jsonify
from recommender import generate_recommendation

planner_bp = Blueprint("planner", __name__)


@planner_bp.route("/api/analyze", methods=["POST"])
def analyze_budget():
    """Analyze income and expenses and return budget recommendations."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send valid budget data."
        }), 400

    try:
        income = float(data.get("income", 0))
        expenses = data.get("expenses", [])

        # Validate income
        if income <= 0:
            return jsonify({
                "error": "Monthly income must be greater than zero."
            }), 400

        # Validate expense list
        if not isinstance(expenses, list):
            return jsonify({
                "error": "Expenses must be provided as a list."
            }), 400

        clean_expenses = []

        for expense in expenses:
            if not isinstance(expense, dict):
                return jsonify({
                    "error": "Each expense must contain a category and amount."
                }), 400

            category = str(expense.get("category", "")).strip()

            if not category:
                return jsonify({
                    "error": "Expense category cannot be empty."
                }), 400

            amount = float(expense.get("amount", 0))

            if amount < 0:
                return jsonify({
                    "error": "Expense amounts cannot be negative."
                }), 400

            clean_expenses.append({
                "category": category,
                "amount": amount
            })

        # Calculate budget summary
        total_expenses = sum(
            expense["amount"] for expense in clean_expenses
        )

        balance = income - total_expenses
        savings_rate = (balance / income) * 100

        # Generate recommendations using your existing function
        recommendations = generate_recommendation(
            income,
            clean_expenses,
            balance
        )

        # Ensure recommendations can be returned as JSON
        if isinstance(recommendations, str):
            recommendations = [recommendations]
        elif not isinstance(recommendations, list):
            recommendations = [
                str(recommendations)
            ]

        return jsonify({
            "success": True,
            "income": round(income, 2),
            "total_expenses": round(total_expenses, 2),
            "balance": round(balance, 2),
            "savings_rate": round(savings_rate, 2),
            "recommendations": recommendations
        }), 200

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid numeric income and expense amounts."
        }), 400

    except Exception:
        return jsonify({
            "error": "An unexpected error occurred during budget analysis."
        }), 500
