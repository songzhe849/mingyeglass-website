
const nodemailer = require("nodemailer");
const qs = require("querystring");

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.redirect(302, "/contact.html"); return; }
  let body = "";
  req.on("data", c => body += c);
  req.on("end", async () => {
    const d = qs.parse(body);
    if (!d.name || !d.email || !d.message) {
      res.writeHead(400, {"Content-Type":"text/html;charset=utf-8"});
      res.end("<h2>Please fill required fields</h2><a href='/contact.html'>Back</a>");
      return;
    }
    const transporter = nodemailer.createTransport({
      host: "smtp.qiye.163.com", port: 465, secure: true,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
    });
    const now = new Date().toLocaleString("zh-CN", {timeZone:"Asia/Shanghai"});
    const html = "<h2>New Inquiry - Mingye Glass</h2><table border='1' cellpadding='8' style='border-collapse:collapse'>"
      + "<tr><td>Name</td><td>" + d.name + "</td></tr>"
      + "<tr><td>Email</td><td>" + d.email + "</td></tr>"
      + "<tr><td>Company</td><td>" + (d.company || "N/A") + "</td></tr>"
      + "<tr><td>Subject</td><td>" + (d.subject || "General") + "</td></tr>"
      + "<tr><td>Time</td><td>" + now + "</td></tr></table>"
      + "<h3>Message:</h3><p>" + d.message + "</p><hr><small>Mingye Glass Website</small>";
    try {
      await transporter.sendMail({
        from: process.env.SMTP_USER, to: process.env.SMTP_USER,
        subject: "New Inquiry from " + d.name,
        html: html
      });
      res.redirect(302, "/thanks.html");
    } catch(e) {
      console.error(e.message);
      res.writeHead(500, {"Content-Type":"text/html;charset=utf-8"});
      res.end("<h2>Send failed, try again later</h2><a href='/contact.html'>Back</a>");
    }
  });
};
