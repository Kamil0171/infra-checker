document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("check-form");
    const input = document.getElementById("url");
    const button = document.getElementById("check-button");
    const resultsContainer = document.getElementById("results-container");
    const formMessage = document.getElementById("form-message");

    if (input && !input.value) {
        input.focus();
    }

    if (!form || !input || !button || !resultsContainer || !formMessage) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const rawUrl = input.value.trim();
        input.value = rawUrl;

        if (!rawUrl) {
            showMessage("Please enter a website URL.", "error");
            return;
        }

        button.disabled = true;
        button.textContent = "Checking...";
        showMessage("Checking website...", "info");

        try {
            const response = await fetch(`/api/check?url=${encodeURIComponent(rawUrl)}`);

            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }

            const data = await response.json();

            resultsContainer.className = "results-grid";
            resultsContainer.innerHTML = buildResultsHtml(data);

            showMessage("Check completed successfully.", "success");
        } catch (error) {
            resultsContainer.className = "";
            resultsContainer.innerHTML = "";

            showMessage(
                "Could not complete the check. Please verify the URL and try again.",
                "error"
            );
        } finally {
            button.disabled = false;
            button.textContent = "Check";
        }
    });

    function showMessage(text, type) {
        formMessage.hidden = false;
        formMessage.textContent = text;
        formMessage.className = `form-message form-message-${type}`;
    }

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function renderValue(value, suffix = "") {
        if (value === null || value === undefined || value === "") {
            return "—";
        }

        return `${escapeHtml(value)}${suffix}`;
    }

    function renderYesNo(value) {
        if (value === null || value === undefined) {
            return "—";
        }

        return value ? "Yes" : "No";
    }

    function formatHttpStatusLabel(statusCode) {
        if (statusCode === null || statusCode === undefined) {
            return "—";
        }

        if (statusCode >= 200 && statusCode < 300) {
            return `${statusCode} (Success)`;
        }

        if (statusCode >= 300 && statusCode < 400) {
            return `${statusCode} (Redirect)`;
        }

        if (statusCode >= 400 && statusCode < 500) {
            return `${statusCode} (Client error)`;
        }

        if (statusCode >= 500) {
            return `${statusCode} (Server error)`;
        }

        return String(statusCode);
    }

    function getHttpStatusBadge(statusCode, isUp) {
        if (!isUp) {
            return `<span class="inline-badge inline-badge-error">Unavailable</span>`;
        }

        if (statusCode >= 200 && statusCode < 300) {
            return `<span class="inline-badge inline-badge-success">2xx</span>`;
        }

        if (statusCode >= 300 && statusCode < 400) {
            return `<span class="inline-badge inline-badge-neutral">3xx</span>`;
        }

        if (statusCode >= 400 && statusCode < 500) {
            return `<span class="inline-badge inline-badge-warning">4xx</span>`;
        }

        if (statusCode >= 500) {
            return `<span class="inline-badge inline-badge-error">5xx</span>`;
        }

        return `<span class="inline-badge inline-badge-neutral">Unknown</span>`;
    }

    function formatIsoDate(isoString) {
        if (!isoString) {
            return "—";
        }

        const date = new Date(isoString);

        if (Number.isNaN(date.getTime())) {
            return escapeHtml(isoString);
        }

        return escapeHtml(
            date.toLocaleString("en-GB", {
                year: "numeric",
                month: "short",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                timeZoneName: "short",
            })
        );
    }

    function getDaysLeftBadge(daysLeft) {
        if (daysLeft === null || daysLeft === undefined) {
            return "";
        }

        if (daysLeft < 0) {
            return `<span class="inline-badge inline-badge-error">Expired</span>`;
        }

        if (daysLeft <= 14) {
            return `<span class="inline-badge inline-badge-error">Urgent</span>`;
        }

        if (daysLeft <= 30) {
            return `<span class="inline-badge inline-badge-warning">Expiring soon</span>`;
        }

        return `<span class="inline-badge inline-badge-success">Healthy</span>`;
    }

    function getHttpBadge(http) {
        if (http.is_up) {
            return `<span class="status-badge status-ok">Responding</span>`;
        }

        return `<span class="status-badge status-error">Issue detected</span>`;
    }

    function getSslBadge(ssl) {
        if (ssl.ssl_enabled === false) {
            return `<span class="status-badge status-neutral">No TLS</span>`;
        }

        if (ssl.ssl_valid) {
            return `<span class="status-badge status-ok">Valid</span>`;
        }

        return `<span class="status-badge status-error">Check failed</span>`;
    }

    function buildResultsHtml(data) {
        const http = data.http;
        const ssl = data.ssl;

        const httpError = http.error
            ? `<p class="error-text">${escapeHtml(http.error)}</p>`
            : "";

        const sslInfo = ssl.ssl_enabled === false
            ? `<p class="neutral-text">SSL/TLS check is skipped for non-HTTPS addresses.</p>`
            : "";

        const sslError = ssl.error
            ? `<p class="error-text">${escapeHtml(ssl.error)}</p>`
            : "";

        return `
            <article class="result-card">
                <div class="section-header centered-header">
                    <h2>HTTP Check</h2>
                    ${getHttpBadge(http)}
                </div>

                <div class="result-list">
                    <div class="result-item">
                        <span>Submitted URL</span>
                        <strong>${escapeHtml(data.submitted_url)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Checked URL</span>
                        <strong>${renderValue(http.checked_url)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Host responded</span>
                        <strong>${renderYesNo(http.is_up)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Status code</span>
                        <strong>
                            ${renderValue(formatHttpStatusLabel(http.status_code))}
                            ${http.status_code !== null && http.status_code !== undefined ? getHttpStatusBadge(http.status_code, http.is_up) : ""}
                        </strong>
                    </div>

                    <div class="result-item">
                        <span>Response time</span>
                        <strong>${renderValue(http.response_time_ms, " ms")}</strong>
                    </div>
                </div>

                ${httpError}
            </article>

            <article class="result-card">
                <div class="section-header centered-header">
                    <h2>SSL/TLS Check</h2>
                    ${getSslBadge(ssl)}
                </div>

                <div class="result-list">
                    <div class="result-item">
                        <span>Checked URL</span>
                        <strong>${renderValue(ssl.checked_url)}</strong>
                    </div>

                    <div class="result-item">
                        <span>SSL/TLS enabled</span>
                        <strong>${renderYesNo(ssl.ssl_enabled)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Certificate valid</span>
                        <strong>${renderYesNo(ssl.ssl_valid)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Expires at</span>
                        <strong>${formatIsoDate(ssl.ssl_expires_at)}</strong>
                    </div>

                    <div class="result-item">
                        <span>Days left</span>
                        <strong>
                            ${renderValue(ssl.ssl_days_left)}
                            ${getDaysLeftBadge(ssl.ssl_days_left)}
                        </strong>
                    </div>
                </div>

                ${sslInfo}
                ${sslError}
            </article>
        `;
    }
});