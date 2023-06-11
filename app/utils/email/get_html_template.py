from ...schemas import email_schema


def get_html_template(params: email_schema.CreateEmailContentSchema) -> str:
    btn_text, btn_link, title, content, link_type, action = params.values()

    html = f"""
    <!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office"
        style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">

<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>New email </title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {{text-decoration: none;}}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup {{ font-size: 100% !important; }}</style><![endif]-->
    <!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]-->
    <style type="text/css">
        #outlook a {{
            padding: 0;
        }}

        .ExternalClass {{
            width: 100%;
        }}

        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {{
            line-height: 100%;
        }}

        .es-button {{
            mso-style-priority: 100 !important;
            text-decoration: none !important;
        }}

        a[x-apple-data-detectors] {{
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }}

        .es-desk-hidden {{
            display: none;
            float: left;
            overflow: hidden;
            width: 0;
            max-height: 0;
            line-height: 0;
            mso-hide: all;
        }}

        [data-ogsb] .es-button {{
            border-width: 0 !important;
            padding: 8px 30px 8px 30px !important;
        }}

        @media only screen and (max-width:600px) {{

            p,
            ul li,
            ol li,
            a {{
                line-height: 150% !important
            }}

            h1,
            h2,
            h3,
            h1 a,
            h2 a,
            h3 a {{
                line-height: 120% !important
            }}

            h1 {{
                font-size: 38px !important;
                text-align: center
            }}

            h2 {{
                font-size: 30px !important;
                text-align: center
            }}

            h3 {{
                font-size: 20px !important;
                text-align: center
            }}

            .es-header-body h1 a,
            .es-content-body h1 a,
            .es-footer-body h1 a {{
                font-size: 38px !important
            }}

            .es-header-body h2 a,
            .es-content-body h2 a,
            .es-footer-body h2 a {{
                font-size: 30px !important
            }}

            .es-header-body h3 a,
            .es-content-body h3 a,
            .es-footer-body h3 a {{
                font-size: 20px !important
            }}

            .es-menu td a {{
                font-size: 14px !important
            }}

            .es-header-body p,
            .es-header-body ul li,
            .es-header-body ol li,
            .es-header-body a {{
                font-size: 14px !important
            }}

            .es-content-body p,
            .es-content-body ul li,
            .es-content-body ol li,
            .es-content-body a {{
                font-size: 14px !important
            }}

            .es-footer-body p,
            .es-footer-body ul li,
            .es-footer-body ol li,
            .es-footer-body a {{
                font-size: 14px !important
            }}

            .es-infoblock p,
            .es-infoblock ul li,
            .es-infoblock ol li,
            .es-infoblock a {{
                font-size: 12px !important
            }}

            *[class="gmail-fix"] {{
                display: none !important
            }}

            .es-m-txt-c,
            .es-m-txt-c h1,
            .es-m-txt-c h2,
            .es-m-txt-c h3 {{
                text-align: center !important
            }}

            .es-m-txt-r,
            .es-m-txt-r h1,
            .es-m-txt-r h2,
            .es-m-txt-r h3 {{
                text-align: right !important
            }}

            .es-m-txt-l,
            .es-m-txt-l h1,
            .es-m-txt-l h2,
            .es-m-txt-l h3 {{
                text-align: left !important
            }}

            .es-m-txt-r img,
            .es-m-txt-c img,
            .es-m-txt-l img {{
                display: inline !important
            }}

            .es-button-border {{
                display: block !important
            }}

            a.es-button,
            button.es-button {{
                font-size: 18px !important;
                display: block !important;
                border-left-width: 0px !important;
                border-right-width: 0px !important
            }}

            .es-btn-fw {{
                border-width: 10px 0px !important;
                text-align: center !important
            }}

            .es-adaptive table,
            .es-btn-fw,
            .es-btn-fw-brdr,
            .es-left,
            .es-right {{
                width: 100% !important
            }}

            .es-content table,
            .es-header table,
            .es-footer table,
            .es-content,
            .es-footer,
            .es-header {{
                width: 100% !important;
                max-width: 600px !important
            }}

            .es-adapt-td {{
                display: block !important;
                width: 100% !important
            }}

            .adapt-img {{
                width: 100% !important;
                height: auto !important
            }}

            .es-m-p0 {{
                padding: 0px !important
            }}

            .es-m-p0r {{
                padding-right: 0px !important
            }}

            .es-m-p0l {{
                padding-left: 0px !important
            }}

            .es-m-p0t {{
                padding-top: 0px !important
            }}

            .es-m-p0b {{
                padding-bottom: 0 !important
            }}

            .es-m-p20b {{
                padding-bottom: 20px !important
            }}

            .es-mobile-hidden,
            .es-hidden {{
                display: none !important
            }}

            tr.es-desk-hidden,
            td.es-desk-hidden,
            table.es-desk-hidden {{
                width: auto !important;
                overflow: visible !important;
                float: none !important;
                max-height: inherit !important;
                line-height: inherit !important
            }}

            tr.es-desk-hidden {{
                display: table-row !important
            }}

            table.es-desk-hidden {{
                display: table !important
            }}

            td.es-desk-menu-hidden {{
                display: table-cell !important
            }}

            .es-menu td {{
                width: 1% !important
            }}

            table.es-table-not-adapt,
            .esd-block-html table {{
                width: auto !important
            }}

            table.es-social {{
                display: inline-block !important
            }}

            table.es-social td {{
                display: inline-block !important
            }}

            .es-desk-hidden {{
                display: table-row !important;
                width: auto !important;
                overflow: visible !important;
                max-height: inherit !important
            }}
        }}
    </style>
</head>

<body
    style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
    <div class="es-wrapper-color" style="background-color:#223748">
        <!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" src="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/88181525777203834.jpg" color="#223748" origin="0.5, 0" position="0.5, 0"></v:fill>
			</v:background>
		<![endif]-->
        <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
            background="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/88181525777203834.jpg"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:no-repeat;background-position:center top;background-image:url(https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/88181525777203834.jpg)">
            <tr style="border-collapse:collapse">
                <td valign="top" style="padding:0;Margin:0">
                    <table class="es-header" cellspacing="0" cellpadding="0" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-header-body"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                    cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse">
                                        <td style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px;background-repeat:no-repeat"
                                            align="left">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:560px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;padding-bottom:5px;padding-top:30px">
                                                                    <h2
                                                                        style="Margin:0;line-height:58px;mso-line-height-rule:exactly;font-family:'lucida sans unicode', 'lucida grande', sans-serif;font-size:58px;font-style:normal;font-weight:normal;color:#ffffff">
                                                                        Welcome</h2>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;font-size:0"><img
                                                                        src="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/43981525778959712.png"
                                                                        alt="to"
                                                                        style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                        title="to" width="42"></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;padding-bottom:15px">
                                                                    <h1
                                                                        style="Margin:0;line-height:69px;mso-line-height-rule:exactly;font-family:'lucida sans unicode', 'lucida grande', sans-serif;font-size:69px;font-style:normal;font-weight:normal;color:#ffffff">
                                                                        Koh</h1>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;padding-bottom:25px">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:tahoma, verdana, segoe, sans-serif;line-height:24px;color:#ffffff;font-size:16px">
                                                                        Awesome clothes for everyone</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff"
                                    align="center"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                                    <tr style="border-collapse:collapse">
                                        <td style="padding:0;Margin:0;padding-top:30px;padding-left:40px;padding-right:40px;background-repeat:no-repeat"
                                            align="left">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:520px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td class="es-m-txt-l" align="left"
                                                                    style="padding:0;Margin:0">
                                                                    <h2
                                                                        style="Margin:0;line-height:34px;mso-line-height-rule:exactly;font-family:'lucida sans unicode', 'lucida grande', sans-serif;font-size:28px;font-style:normal;font-weight:normal;color:#333333">
                                                                        {title}&nbsp;</h2>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td class="es-m-txt-l" align="left"
                                                                    style="padding:0;Margin:0;font-size:0"><a
                                                                        target="_blank"
                                                                        href="https://esputnik.com/viewInBrowser"
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            src="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/99301524564595313.png"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="75"></a></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td align="left"
                                                                    style="padding:0;Margin:0;padding-top:15px">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'lucida sans unicode', 'lucida grande', sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                        Below is your {link_type} link,&nbsp;</p>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td align="left"
                                                                    style="padding:0;Margin:0;padding-bottom:10px;padding-top:25px">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'lucida sans unicode', 'lucida grande', sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                        {content}</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr style="border-collapse:collapse">
                                        <td align="left"
                                            style="Margin:0;padding-top:20px;padding-bottom:40px;padding-left:40px;padding-right:40px">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:520px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="left"
                                                                    style="padding:0;Margin:0;padding-top:5px"><span
                                                                        class="es-button-border"
                                                                        style="border-style:solid;border-color:#333333;background:#333333;border-width:0px;display:inline-block;border-radius:5px;width:auto"><a
                                                                            href="{btn_link}"
                                                                            class="es-button" target="_blank"
                                                                            style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:16px;border-style:solid;border-color:#333333;border-width:8px 30px 8px 30px;display:inline-block;background:#333333;border-radius:5px;font-family:'lucida sans unicode', 'lucida grande', sans-serif;font-weight:normal;font-style:normal;line-height:19px;width:auto;text-align:center">{btn_text}</a></span></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                        <tr style="border-collapse:collapse"></tr>
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff"
                                    align="center"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                                    <tr style="border-collapse:collapse">
                                        <td style="padding:0;Margin:0;background-color:#fdf7f7" bgcolor="#fdf7f7"
                                            align="left">
                                            <!--[if mso]><table style="width:600px" cellpadding="0" 
                            cellspacing="0"><tr><td style="width:200px" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                                <tr style="border-collapse:collapse">
                                                    <td align="center" style="padding:0;Margin:0;width:200px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;font-size:0px"><a
                                                                        target="_blank" href="https://viewstripo.email/"
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            class="adapt-img"
                                                                            src="https://wlases.stripocdn.email/content/guids/e0b3b1e1-6f30-4a2a-b732-b4b35d7b4946/images/andiriegerx9h9gupms48unsplash.jpg"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="199"></a></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td><td style="width:200px" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                                <tr style="border-collapse:collapse">
                                                    <td class="es-m-p0r" align="center"
                                                        style="padding:0;Margin:0;width:200px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;font-size:0px"><a
                                                                        target="_blank" href="https://viewstripo.email/"
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            class="adapt-img"
                                                                            src="https://wlases.stripocdn.email/content/guids/e0b3b1e1-6f30-4a2a-b732-b4b35d7b4946/images/austinwadelnyyi0u3ounsplash.jpg"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="200"></a></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td><td style="width:0px"></td><td style="width:200px" valign="top"><![endif]-->
                                            <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                                <tr style="border-collapse:collapse">
                                                    <td align="center" style="padding:0;Margin:0;width:200px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="left"
                                                                    style="padding:0;Margin:0;font-size:0px"><a
                                                                        target="_blank" href="https://viewstripo.email/"
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            class="adapt-img"
                                                                            src="https://wlases.stripocdn.email/content/guids/e0b3b1e1-6f30-4a2a-b732-b4b35d7b4946/images/andiriegerze_k7vn0pnmunsplash.jpg"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="199"></a></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td></tr></table><![endif]-->
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff"
                                    align="center"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                                    <tr style="border-collapse:collapse">
                                        <td align="left"
                                            style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:520px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="left" style="padding:0;Margin:0">
                                                                    <h2
                                                                        style="Margin:0;line-height:29px;mso-line-height-rule:exactly;font-family:'times new roman', times, baskerville, georgia, serif;font-size:24px;font-style:normal;font-weight:normal;color:#333333">
                                                                        Get our App</h2>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr style="border-collapse:collapse">
                                        <td align="left"
                                            style="Margin:0;padding-top:20px;padding-bottom:40px;padding-left:40px;padding-right:40px">
                                            <!--[if mso]><table style="width:520px" cellpadding="0" 
                            cellspacing="0"><tr><td style="width:150px" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                                <tr style="border-collapse:collapse">
                                                    <td class="es-m-p0r es-m-p20b" align="center"
                                                        style="padding:0;Margin:0;width:130px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;font-size:0"><div
                                                                        
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            class="adapt-img"
                                                                            src="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/81101525781549293.png"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="130"></div></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="es-hidden" style="padding:0;Margin:0;width:20px"></td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td><td style="width:130px" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                                <tr style="border-collapse:collapse">
                                                    <td class="es-m-p20b" align="center"
                                                        style="padding:0;Margin:0;width:130px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;font-size:0"><div
                                                                        
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#999999;font-size:16px"><img
                                                                            class="adapt-img"
                                                                            src="https://wlases.stripocdn.email/content/guids/CABINET_6ebdc9f620b6c98ec92e579217982603/images/74371525781549159.png"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="130"></div></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td><td style="width:20px"></td><td style="width:220px" valign="top"><![endif]-->
                                            <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                                <tr style="border-collapse:collapse">
                                                    <td align="center" style="padding:0;Margin:0;width:220px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td class="es-m-txt-c" align="left"
                                                                    style="padding:0;Margin:0">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;color:#666666;font-size:14px">
                                                                        Download app to follow updates. Our app is free
                                                                        and is ethical.</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td></tr></table><![endif]-->
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table cellpadding="0" cellspacing="0" class="es-footer" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-footer-body" cellspacing="0" cellpadding="0" align="center"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                                    <tr style="border-collapse:collapse">
                                        <td align="left"
                                            style="padding:0;Margin:0;padding-left:10px;padding-right:10px;padding-top:20px">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:580px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-bottom:10px;font-size:0">
                                                                    <table class="es-table-not-adapt es-social"
                                                                        cellspacing="0" cellpadding="0"
                                                                        role="presentation"
                                                                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                        <tr style="border-collapse:collapse">
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0;padding-right:10px">
                                                                                <img title="Instagram"
                                                                                    src="https://wlases.stripocdn.email/content/assets/img/social-icons/rounded-white-bordered/instagram-rounded-white-bordered.png"
                                                                                    alt="Inst" width="32"
                                                                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                            </td>
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0;padding-right:10px">
                                                                                <img title="Youtube"
                                                                                    src="https://wlases.stripocdn.email/content/assets/img/social-icons/rounded-white-bordered/youtube-rounded-white-bordered.png"
                                                                                    alt="Yt" width="32"
                                                                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                            </td>
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0;padding-right:10px">
                                                                                <img title="Pinterest"
                                                                                    src="https://wlases.stripocdn.email/content/assets/img/social-icons/rounded-white-bordered/pinterest-rounded-white-bordered.png"
                                                                                    alt="P" width="32"
                                                                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                            </td>
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0"><img
                                                                                    title="Facebook"
                                                                                    src="https://wlases.stripocdn.email/content/assets/img/social-icons/rounded-white-bordered/facebook-rounded-white-bordered.png"
                                                                                    alt="Fb" width="32"
                                                                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-top:10px">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;color:#EFEFEF;font-size:14px">
                                                                        You're receiving this email because you asked us
                                                                        about {action}.<br></p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                        <tr style="border-collapse:collapse">
                            <td align="center" style="padding:0;Margin:0">
                                <table class="es-content-body"
                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                    cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse">
                                        <td align="left"
                                            style="Margin:0;padding-left:20px;padding-right:20px;padding-top:30px;padding-bottom:30px">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                <tr style="border-collapse:collapse">
                                                    <td valign="top" align="center"
                                                        style="padding:0;Margin:0;width:560px">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                            role="presentation"
                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                            <tr style="border-collapse:collapse">
                                                                <td align="center" style="padding:0;Margin:0">
                                                                    <p
                                                                        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:54px;color:#f6f5f5;font-size:36px">
                                                                        <strong>Koh.</strong>
                                                                    </p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>
</body>

</html>
    """
    return html
