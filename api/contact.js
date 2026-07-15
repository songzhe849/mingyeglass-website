
module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.writeHead(200, {"Content-Type": "text/html;charset=utf-8"});
    res.end("<h1>Contact API - Use POST to submit</h1>");
    return;
  }
  
  let body = "";
  req.on("data", c => body += c);
  req.on("end", async () => {
    const qs = require("querystring");
    const d = qs.parse(body);
    
    console.log("Contact form received:", JSON.stringify(d));
    
    // Try to send email via SMTP
    try {
      const transporter = require("nodemailer").createTransport({
        host: "smtp.qiye.163.com", port: 465, secure: true,
        auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
      });
      
      await transporter.sendMail({
        from: process.env.SMTP_USER, to: process.env.SMTP_USER,
        subject: "New Inquiry from " + (d.name || "Visitor"),
        html: "<h2>New Inquiry</h2><p><b>Name:</b> " + (d.name || "N/A") + "</p>" +
              "<p><b>Email:</b> " + (d.email || "N/A") + "</p>" +
              "<p><b>Company:</b> " + (d.company || "N/A") + "</p>" +
              "<p><b>Subject:</b> " + (d.subject || "General") + "</p>" +
              "<p><b>Message:</b><br>" + (d.message || "") + "</p>"
      });
      
      console.log("Email sent successfully");
    } catch(e) {
      console.log("Email send failed (non-fatal):", e.message);
    }
    
    // Always return success to the user
    res.writeHead(200, {"Content-Type": "text/html;charset=utf-8"});
    res.end("<html><body style='font-family:Arial;text-align:center;padding:60px'>" +
            "<h1 style='color:#c4956a'>Thank You!</h1>" +
            "<p>Your inquiry has been submitted. We will respond within 24 hours.</p>" +
            "<a href='/' style='color:#c4956a'>Back to Home</a></body></html>");
  });
};
