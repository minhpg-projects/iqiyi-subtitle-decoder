const decrypt = require('./libmonalisa-v3.0.6-browser');
const crypto = require('crypto')
const { default: srtParser2 } = require("srt-parser-2")
const got = require('got')
const buffertrim = require('buffertrim') 

module.exports = async (req,res) => {
    url = req.query.url
    if(!url) {
        throw new Error('please provide an url')
    }
    console.log(`downloading subtitle from ${url}`)
    const response = await got(url)
    const key = await decrypt(process.env.LIBMONALISA_LICENSE_KEY)
    var iv = Buffer.from(Uint8Array.from([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    lines = []
    var parser = new srtParser2()
    var result = parser.fromSrt(response.body)
    for (line of result) {
        var decipher = crypto.createDecipheriv('aes-128-cbc', key, iv)
        decipher.setAutoPadding(false)
        var bufPlaintextB64padded = Buffer.concat([
            decipher.update(line.text, 'base64'),
            decipher.final()
        ]);
        bufPlaintextB64 = buffertrim.trimEnd(bufPlaintextB64padded)
        line.text = bufPlaintextB64padded.toString('utf-8').trim()
        lines.push(`${line.id}
${line.startTime} --> ${line.endTime}
${line.text}`)
    }
    console.log(lines)

    res.setHeader('Content-Type', 'text/plain')
    res.send(lines.join('\n\n'))
    res.end()
}