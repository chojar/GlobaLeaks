describe("admin configure, add, and delete tenants", function() {
  it("should add new tenant", async function() {
    await browser.gl.utils.login_admin();

    await browser.setLocation("admin/tenants");

    var add_tenant = async function(tenant_label) {
      await element(by.css(".show-add-tenant-btn")).click();
      await element(by.model("newTenant.label")).sendKeys(tenant_label);
      await element(by.id("add-btn")).click();
      await browser.gl.utils.waitUntilPresent(by.xpath(".//*[text()='" + tenant_label + "']"));
    };

    await add_tenant("Tenant 2");
    await add_tenant("Tenant 3");
  });

  it("should del existing tenants", async function() {
    await element.all((by.cssContainingText("button", "Delete"))).last().click();
    await element(by.id("modal-action-ok")).click();

    // TODO check that the tenant is actually gone
  });
});
