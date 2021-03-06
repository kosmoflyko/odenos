/*
 * Copyright 2015 NEC Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.o3project.odenos.core.component.network.flow.ofpflow;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.when;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.mockito.Mockito;
import org.msgpack.type.Value;
import org.msgpack.type.ValueFactory;

import java.util.HashMap;
import java.util.Map;

public class OFPFlowActionPushPbbTest {

  private OFPFlowActionPushPbb target;

  /**
   * @throws java.lang.Exception throws Exception in targets
   */
  @BeforeClass
  public static void setUpBeforeClass() throws Exception {
  }

  /**
   * @throws java.lang.Exception throws Exception in targets
   */
  @AfterClass
  public static void tearDownAfterClass() throws Exception {
  }

  /**
   * @throws java.lang.Exception throws Exception in targets
   */
  @Before
  public void setUp() throws Exception {
    target = spy(new OFPFlowActionPushPbb());
  }

  /**
   * @throws java.lang.Exception throws Exception in targets
   */
  @After
  public void tearDown() throws Exception {
    target = null;
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#OFPFlowActionPushPbb()}
   * .
   */
  @Test
  public final void testOFPFlowActionPushPbb() {
    OFPFlowActionPushPbb target = new OFPFlowActionPushPbb();

    assertThat(target.getEthType(), is(OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#OFPFlowActionPushPbb(Integer)}
   * .
   */
  @Test
  public final void testOFPFlowActionPushPbbInteger() {
    OFPFlowActionPushPbb target = new OFPFlowActionPushPbb(OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE);

    assertThat(target.getEthType(), is(new Integer(OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE)));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#validate()}
   * .
   */
  @Test
  public final void testValidateNull() {
    OFPFlowActionPushPbb target = new OFPFlowActionPushPbb();
    boolean result = target.validate();

    assertThat(result, is(true));

    target = new OFPFlowActionPushPbb(10);
    result = target.validate();

    assertThat(result, is(true));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#getType()}
   * .
   */
  @Test
  public final void testGetType() {
    assertThat(target.getType(), is("OFPFlowActionPushPbb"));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#readValue(org.msgpack.type.Value)}
   * .
   */
  @Test
  public final void testReadValue() {
    /*
     * set
     */
    Value[] valueArray = new Value[2];
    valueArray[0] = ValueFactory.createRawValue("eth_type");
    valueArray[1] = ValueFactory.createIntegerValue(OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE);

    Value value = Mockito.mock(Value.class);

    when(value.asMapValue()).thenReturn(ValueFactory.createMapValue(valueArray));

    /*
     * test
     */
    boolean result = target.readValue(value);

    /*
     * check
     */
    assertThat(result, is(true));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#writeValueSub(java.util.Map)}
   * .
   */
  @Test
  public final void testWriteValueSub() {
    Map<String, Value> values = new HashMap<String, Value>();

    boolean result = target.writeValueSub(values);

    assertThat(result, is(true));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#equals(java.lang.Object)}
   * .
   */
  @Test
  public final void testEquals() {
    OFPFlowActionPushPbb obj = target;

    boolean result = target.equals(obj);

    assertThat(result, is(true));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#equals(java.lang.Object)}
   * .
   */
  @Test
  public final void testEqualsNull() {
    boolean result = target.equals(null);

    assertThat(result, is(false));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#equals(java.lang.Object)}
   * .
   */
  @Test
  public final void testEqualsInstanceofFalse() {
    boolean result = target.equals("String");

    assertThat(result, is(false));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#equals(java.lang.Object)}
   * .
   */
  @Test
  public final void testEqualsSuperFalse() {
    OFPFlowActionPushPbb obj = new OFPFlowActionPushPbb();
    doReturn("false").when(target).getType();

    boolean result = target.equals(obj);

    assertThat(result, is(false));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#equals(java.lang.Object)}
   * .
   */
  @Test
  public final void testEqualsNotEqualsGroupId() {
    OFPFlowActionPushPbb obj = new OFPFlowActionPushPbb();

    boolean result = target.equals(obj);

    assertThat(result, is(false));
  }

  /**
   * Test method for
   * {@link org.o3project.odenos.core.component.network.flow.ofpflow.OFPFlowActionPushPbb#toString()}
   * .
   */
  @Test
  public final void testToString() {

    /*
     * setting
     */
    target = new OFPFlowActionPushPbb(OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE);

    /*
     * test
     */
    String result = target.toString();

    /*
     * check
     */
    String expect = String.format("[ethType=%s]", OFPFlowActionPushPbb.DEFAULT_ETHER_TYPE);
    assertThat(result.endsWith(expect), is(true));

  }

}
