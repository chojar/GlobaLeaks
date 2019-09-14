describe("whistleblower navigate home page", function() {
  it("should see page properly internationalized in EN", async function() {
    await browser.get("/#/?lang=en");
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT1_IT")))).toBe(false);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT2_IT")))).toBe(false);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT1_EN")))).toBe(true);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT2_EN")))).toBe(true);

  });

  it("should see page properly internationalized in IT", async function() {
    await browser.get("/#/?lang=it");
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT1_IT")))).toBe(true);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT2_IT")))).toBe(true);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT1_EN")))).toBe(false);
    expect(await browser.isElementPresent(element(by.cssContainingText("div", "TEXT2_EN")))).toBe(false);
  });
});
