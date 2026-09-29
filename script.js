function isValidURL(url) {
    try {
        const parsed = new URL(url);

        return (
            (parsed.protocol === "http:" || parsed.protocol === "https:") &&
            parsed.hostname.includes(".")
        );

    } catch {
        return false;
    }
}

//enter key support
document.getElementById("urlInput").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        e.preventDefault();
        checkURL();
    }
});

async function checkURL() {

    let url = document.getElementById("urlInput").value.trim();

    if (!url) {
        Swal.fire({
            icon: "warning",
            title: "Enter a URL first"
        });
        return;
    }

    //auto add https if missing
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        url = "https://" + url;
    }

    if (!isValidURL(url)) {
        Swal.fire({
            icon: "error",
            title: "Invalid URL"
        });
        return;
    }

    const startTime = Date.now();

    //loading or analyzing part
    Swal.fire({
        title: "Analyzing URL...",
        html: "Scanning for threats...",
        allowOutsideClick: false,
        showConfirmButton: false,
        backdrop: `rgba(15,23,42,0.85)`,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        const res = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await res.json();

        const elapsed = Date.now() - startTime;
        const delay = Math.max(900 - elapsed, 0);

        setTimeout(() => {

            Swal.close();

            if (data.error) {
                Swal.fire({
                    icon: "error",
                    title: "Backend Error",
                    text: data.error
                });
                return;
            }

            //safe
            if (data.prediction && data.prediction.toLowerCase() === "safe") {

                Swal.fire({
                    icon: "success",
                    title: "Safe Website",
                    html: `
                        <b>No threats detected</b><br><br>
                        Confidence: ${((1 - data.malicious_probability) * 100).toFixed(1)}
                    `,
                    confirmButtonColor: "#22c55e",
                    showClass: { popup: "swal2-show animate-popup" }
                });

            } else {

                //malicious
                Swal.fire({
                    icon: "error",
                    title: "Malicious URL Detected",
                    html: `
                        <b>This site may be dangerous!</b><br><br>
                        Risk Score: ${data.malicious_probability.toFixed(2)}
                    `,
                    confirmButtonColor: "#ef4444",
                    showClass: { popup: "swal2-show animate-popup" }
                });

            }

        }, delay);

    } catch (err) {

        Swal.close();

        Swal.fire({
            icon: "error",
            title: "Server Error",
            text: "Make sure backend is running"
        });

    }
}