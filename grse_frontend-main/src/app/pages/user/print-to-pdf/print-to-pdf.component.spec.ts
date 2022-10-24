import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrintToPdfComponent } from './print-to-pdf.component';

describe('PrintToPdfComponent', () => {
  let component: PrintToPdfComponent;
  let fixture: ComponentFixture<PrintToPdfComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrintToPdfComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PrintToPdfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
