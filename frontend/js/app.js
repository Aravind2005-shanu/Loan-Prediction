/**
 * Loan Prediction Web Application — Frontend Logic
 * Vanilla JavaScript (No React, No external dependencies)
 */

document.addEventListener("DOMContentLoaded", () => {
    // Form and input elements
    const loanForm = document.getElementById("loanForm");
    const submitBtn = document.getElementById("submitBtn");
    
    // Status containers
    const loadingContainer = document.getElementById("loadingContainer");
    const resultContainer = document.getElementById("resultContainer");
    const resultIcon = document.getElementById("resultIcon");
    const resultTitle = document.getElementById("resultTitle");
    const resultDetails = document.getElementById("resultDetails");
    const resetBtn = document.getElementById("resetBtn");
    
    // Error container
    const errorContainer = document.getElementById("errorContainer");
    const errorTitle = document.getElementById("errorTitle");
    const errorMsg = document.getElementById("errorMsg");
    const retryBtn = document.getElementById("retryBtn");

    // Form fields dictionary
    const fields = {
        gender: document.getElementById("gender"),
        married: document.getElementById("married"),
        dependents: document.getElementById("dependents"),
        education: document.getElementById("education"),
        self_employed: document.getElementById("self_employed"),
        applicant_income: document.getElementById("applicant_income"),
        coapplicant_income: document.getElementById("coapplicant_income"),
        loan_amount: document.getElementById("loan_amount"),
        loan_amount_term: document.getElementById("loan_amount_term"),
        credit_history: document.getElementById("credit_history"),
        property_area: document.getElementById("property_area")
    };

    // Attach real-time input event listeners to clear error states
    Object.keys(fields).forEach(key => {
        const field = fields[key];
        if (!field) return;

        const clearError = () => {
            field.classList.remove("is-invalid");
            const errSpan = document.getElementById(`err-${key}`);
            if (errSpan) errSpan.textContent = "";
        };

        field.addEventListener("input", clearError);
        field.addEventListener("change", clearError);
    });

    /**
     * Validates all form inputs.
     * Returns true if form is valid, false otherwise.
     */
    function validateForm() {
        let isValid = true;

        // Reset errors first
        Object.keys(fields).forEach(key => {
            const errSpan = document.getElementById(`err-${key}`);
            if (errSpan) errSpan.textContent = "";
            fields[key].classList.remove("is-invalid");
        });

        // 1. Gender
        if (!fields.gender.value) {
            showFieldError("gender", "Please select applicant gender.");
            isValid = false;
        }

        // 2. Married
        if (!fields.married.value) {
            showFieldError("married", "Please select marital status.");
            isValid = false;
        }

        // 3. Dependents
        if (!fields.dependents.value) {
            showFieldError("dependents", "Please select number of dependents.");
            isValid = false;
        }

        // 4. Education
        if (!fields.education.value) {
            showFieldError("education", "Please select education qualification.");
            isValid = false;
        }

        // 5. Self Employed
        if (!fields.self_employed.value) {
            showFieldError("self_employed", "Please select employment status.");
            isValid = false;
        }

        // 6. Applicant Income
        const incomeVal = parseFloat(fields.applicant_income.value);
        if (isNaN(incomeVal) || incomeVal < 0) {
            showFieldError("applicant_income", "Please enter a valid monthly income (minimum 0).");
            isValid = false;
        }

        // 7. Coapplicant Income
        const coIncomeVal = parseFloat(fields.coapplicant_income.value);
        if (isNaN(coIncomeVal) || coIncomeVal < 0) {
            showFieldError("coapplicant_income", "Please enter a valid coapplicant income (enter 0 if none).");
            isValid = false;
        }

        // 8. Loan Amount
        const loanAmtVal = parseFloat(fields.loan_amount.value);
        if (isNaN(loanAmtVal) || loanAmtVal <= 0) {
            showFieldError("loan_amount", "Please enter a valid loan amount in thousands (e.g. 150).");
            isValid = false;
        }

        // 9. Loan Term
        if (!fields.loan_amount_term.value) {
            showFieldError("loan_amount_term", "Please select a loan term duration.");
            isValid = false;
        }

        // 10. Credit History
        if (fields.credit_history.value === "") {
            showFieldError("credit_history", "Please select credit history status.");
            isValid = false;
        }

        // 11. Property Area
        if (!fields.property_area.value) {
            showFieldError("property_area", "Please select property location area.");
            isValid = false;
        }

        return isValid;
    }

    function showFieldError(key, message) {
        const field = fields[key];
        const errSpan = document.getElementById(`err-${key}`);
        if (field) field.classList.add("is-invalid");
        if (errSpan) errSpan.textContent = message;
    }

    /**
     * Form submission handler
     */
    loanForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        // Construct JSON payload
        const payload = {
            gender: fields.gender.value,
            married: fields.married.value,
            dependents: fields.dependents.value,
            education: fields.education.value,
            self_employed: fields.self_employed.value,
            applicant_income: parseFloat(fields.applicant_income.value),
            coapplicant_income: parseFloat(fields.coapplicant_income.value),
            loan_amount: parseFloat(fields.loan_amount.value),
            loan_amount_term: parseFloat(fields.loan_amount_term.value),
            credit_history: parseFloat(fields.credit_history.value),
            property_area: fields.property_area.value
        };

        // Transition UI to Loading state
        setSubmittingState(true);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const msg = errorData.error || errorData.detail || "We couldn't process this application. Please verify the information and try again.";
                showErrorState("Prediction Failed", msg);
                return;
            }

            const data = await response.json();
            
            if (data.success && data.prediction) {
                showResultState(data.prediction, data.details);
            } else {
                showErrorState("Prediction Failed", data.error || "Unexpected response format received from server.");
            }

        } catch (err) {
            console.error("Network or API call exception:", err);
            showErrorState("Connection Error", "Unable to connect to the prediction server. Please verify your connection and try again.");
        } finally {
            setSubmittingState(false);
        }
    });

    /**
     * Updates loading & submission UI controls
     */
    function setSubmittingState(isSubmitting) {
        if (isSubmitting) {
            submitBtn.disabled = true;
            loanForm.classList.add("hidden");
            resultContainer.classList.add("hidden");
            errorContainer.classList.add("hidden");
            loadingContainer.classList.remove("hidden");
        } else {
            submitBtn.disabled = false;
            loadingContainer.classList.add("hidden");
        }
    }

    /**
     * Renders Success / Rejection result screen
     */
    function showResultState(predictionText, detailsText) {
        loanForm.classList.add("hidden");
        loadingContainer.classList.add("hidden");
        errorContainer.classList.add("hidden");

        resultContainer.classList.remove("hidden", "approved", "rejected");

        if (predictionText === "Loan Approved") {
            resultContainer.classList.add("approved");
            resultIcon.textContent = "✓";
            resultTitle.textContent = "LOAN APPROVED";
        } else {
            resultContainer.classList.add("rejected");
            resultIcon.textContent = "✕";
            resultTitle.textContent = "LOAN NOT APPROVED";
        }

        resultDetails.textContent = detailsText || (
            predictionText === "Loan Approved" 
                ? "The machine learning model predicts that this application meets the learned approval pattern."
                : "The machine learning model predicts that this application does not meet the learned approval pattern."
        );
    }

    /**
     * Renders Error screen
     */
    function showErrorState(title, message) {
        loanForm.classList.add("hidden");
        loadingContainer.classList.add("hidden");
        resultContainer.classList.add("hidden");

        errorTitle.textContent = title;
        errorMsg.textContent = message;
        errorContainer.classList.remove("hidden");
    }

    /**
     * Reset form and return to input view
     */
    function resetApplication() {
        resultContainer.classList.add("hidden");
        errorContainer.classList.add("hidden");
        loadingContainer.classList.add("hidden");
        
        loanForm.reset();
        
        // Reset field error spans and classes
        Object.keys(fields).forEach(key => {
            const errSpan = document.getElementById(`err-${key}`);
            if (errSpan) errSpan.textContent = "";
            if (fields[key]) fields[key].classList.remove("is-invalid");
        });

        loanForm.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    resetBtn.addEventListener("click", resetApplication);
    retryBtn.addEventListener("click", resetApplication);
});
