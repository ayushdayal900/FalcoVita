import { test, expect } from '@playwright/test';

test('Add a new todo', async ({ page }) => {
  await page.goto('https://todomvc.com/examples/typescript-react/#/');

  await page.locator('.new-todo').fill('Buy groceries');
  await page.keyboard.press('Enter');

  await expect(page.locator('li')).toContainText('Buy groceries');
});


test('Check complete', async ({ page }) => {
  await page.goto('https://todomvc.com/examples/typescript-react/#/');
  await page.locator('.new-todo');
  await page.keyboard.press('Enter');
  await expect(page.locator('li')).toContainText('Buy groceries');
  
});
