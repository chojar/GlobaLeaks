describe("Admin configure custom CSS", function() {
  it("should be able to see the LogoBox", async function() {
    var EC = protractor.ExpectedConditions;

    await browser.get("/");
    await browser.wait(EC.visibilityOf($("#LogoBox")));
  });

  it("should not be able to see the LogoBox when loaded in embedded mode", async function() {
    if (!browser.gl.utils.testFileUpload()) {
      return;
    }

    var EC = protractor.ExpectedConditions;

    await browser.get("/#/login?embed=true");
    await browser.wait(EC.invisibilityOf($("#LogoBox")));
  });

  it("should be able to configure a custom CSS", async function() {
    if (!browser.gl.utils.testFileUpload()) {
      return;
    }

    await browser.gl.utils.login_admin();

    var EC = protractor.ExpectedConditions;

    await browser.setLocation("admin/content");

    await browser.gl.utils.waitUntilPresent(by.cssContainingText("a", "Theme customization"));

    await element(by.cssContainingText("a", "Theme customization")).click();

    var customCSSFile = browser.gl.utils.makeTestFilePath("custom_css.css");

    await element(by.css("div.uploadfile.file-css")).element(by.css("input")).sendKeys(customCSSFile);

    await browser.gl.utils.waitUntilPresent(by.cssContainingText("label", "Project name"));

    await element(by.cssContainingText("a", "Theme customization")).click();

    if (browser.gl.utils.testFileDownload() && browser.gl.utils.verifyFileDownload()) {
      var actualFile = browser.gl.utils.makeSavedFilePath("custom_stylesheet.css");
      await element(by.css("div.uploadfile.file-css")).element(by.cssContainingText("a", "Download")).click();
      await browser.gl.utils.testFileEquality(customCSSFile, actualFile);
    }
  });

  it("should not be able to see the LogoBox if hidden by css", async function() {
    if (!browser.gl.utils.testFileUpload()) {
      return;
    }

    var EC = protractor.ExpectedConditions;
    await browser.get("/");
    await browser.wait(EC.invisibilityOf($("#LogoBox")));
  });

  it("should be able to reset CSS customization", async function() {
    if (!browser.gl.utils.testFileUpload()) {
      return;
    }

    await browser.gl.utils.login_admin();
    await browser.setLocation("admin/content");
    await element(by.cssContainingText("a", "Theme customization")).click();
    await element.all(by.cssContainingText("button", "Delete")).first().click();

    // wait until redirect to the first tab of the admin/content section
    await browser.gl.utils.waitUntilPresent(by.cssContainingText("label", "Project name"));
  });

  it("should be able to see again the LogoBox", async function() {
    if (!browser.gl.utils.testFileUpload()) {
      return;
    }

    var EC = protractor.ExpectedConditions;
    await browser.get("/");
    await browser.wait(EC.visibilityOf($("#LogoBox")));
  });
});
